#!/usr/bin/env python

import os
import json
import hashlib
import random
import shutil
from tempfile import NamedTemporaryFile


from flask import Flask, request, render_template, render_template_string, redirect, url_for
from urlparse import urlparse

from util import fold_left
import string

app = Flask(__name__)


debug = False


precomputed_hash_table = {}


# Unfortunately in python the hashes of strings are not stable over multiple runs as they are randomized to prevent
# hash table DOS because of collision attacks. Therefore we have to use our own stable implementation to be able to
# match strings between runs.
def ensure_hash_tree():
    global precomputed_hash_table
    if len(precomputed_hash_table) == 0:
        return update_hash_tree()
    return True



def update_hash_tree():
    global precomputed_hash_table
    if not os.path.isfile('../rw/hash_table.json'):
        return True
    try:
        with open('../rw/hash_table.json', 'r') as f:
            hash_tree = json.load(f)
            precomputed_hash_table.update(hash_tree)
            return True
    except OSError:
        return False


def writeout_hash_tree():
    global precomputed_hash_table
    with NamedTemporaryFile(dir=os.path.abspath('../rw/'), delete=False) as f:
        name = f.name
        json.dump(precomputed_hash_table, f)
        f.flush()
    os.rename(name, '../rw/hash_table.json')

"""
def ensure_hash_tree():
    pass



def update_hash_tree():
    pass


def writeout_hash_tree():
    pass
"""

def fast_str_hash(s):
    ensure_hash_tree()
    precomputed_values = []
    for c in s:
        if c not in precomputed_hash_table:
            update_hash_tree()
            if c not in precomputed_hash_table:
                h = int(hashlib.sha1(c).hexdigest(), 16)
                precomputed_hash_table[c] = h
                writeout_hash_tree()

        precomputed_values.append(precomputed_hash_table[c])
    return fold_left(precomputed_values)(0)(lambda s, v: s + v) & ((0x1 << 64) - 1)


# stolen from django:http.py
def is_safe_url(url, host=None):
    """
    Return ``True`` if the url is a safe redirection (i.e. it doesn't point to
    a different host and uses a safe scheme).
    Always returns ``False`` on an empty url.
    """
    if not url:
        return False
    url = url.strip()
    # Chrome treats \ completely as /
    url = url.replace('\\', '/')
    # Chrome considers any URL with more than two slashes to be absolute, but
    # urlparse is not so flexible. Treat any url with three slashes as unsafe.
    if url.startswith('///'):
        return False
    url_info = urlparse(url)
    # Forbid URLs like http:///example.com - with a scheme, but without a hostname.
    # In that URL, example.com is not the hostname but, a path component. However,
    # Chrome will still consider example.com to be the hostname, so we must not
    # allow this syntax.
    if not url_info.netloc and url_info.scheme:
        return False
    return ((not url_info.netloc or url_info.netloc == host) and
            (not url_info.scheme or url_info.scheme in ['http', 'https']))


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url

    url = request.referrer
    if url and is_safe_url(url):
        return url

    return '/'


# @kevin: unsafe!!
#def make_background():
#    return render_template('background.html', redirect=get_safe_redirect(), content="{{content|safe}}")


def error(message=None):
    if debug and message is not None:
        return render_template_string('error.html', redirect=get_safe_redirect(), content=message)
    return redirect('/nice_try')


def validate_text(text):
    return all(c in string.ascii_letters + string.digits + '_' for c in text)


def validate_secret(s):
    return validate_text(s) and len(s) == 32


def validate_flag(s):
    return validate_text(s) and len(s) == 16


def validate_flag_id(s):
    return validate_text(s)


def store_flag(secret, flag):
    flags_dir = os.path.abspath('../append/flags/')
    if not os.path.isdir(flags_dir):
        os.makedirs(flags_dir)
    with NamedTemporaryFile(mode="w+b", dir=flags_dir, prefix='flg', delete=False) as f:
        json.dump({'secret': secret, 'flag': flag}, f)
        return os.path.basename(f.name)

@app.route("/", methods=["GET"])
@app.route("/index.html", methods=["GET"])
@app.route("/see_unicorn", methods=["GET"])
def see_unicorn():
    # import ipdb; ipdb.set_trace()
    if 'id' in request.args and 'secret' in request.args:
        flag_id = request.args.get('id', '')
        secret = request.args.get('secret', '')
        if not validate_flag_id(flag_id) or not validate_secret(secret):
            return error('invalid flag_id: {} or secret: {}'.format(list(flag_id), list(secret)))
        else:
            try:
                with open(os.path.abspath('../append/flags/' + flag_id), 'r') as f:
                    data = json.load(f)
                    if fast_str_hash(data['secret']) != fast_str_hash(secret):
                        return error('wrong secret')
                    else:
                        fg = render_template('fg_see_unicorn.html', flag=data['flag'], rand_val=random.randint(0, 3), redirect=get_safe_redirect())
            except Exception as ex:
                return error('file {} not found: {}'.format(os.path.abspath('../append/flags/' + flag_id), ex))
    else:
        fg = render_template('fg_view_unicorn.html', redirect=get_safe_redirect())
    return fg


@app.route("/catch_unicorn", methods=["POST", "GET"])
def catch_unicorn():
    # import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        secret = request.form.get('secret', '')
        flag = request.form.get('name', '')
        # print "Secret: {}, Flag: {}".format(secret, flag)
        if validate_secret(secret) and validate_flag(flag):
            flag_id = store_flag(secret, flag)
            fg = render_template('fg_jailed_unicorn.html', flag_id=flag_id, secret=secret, flag=flag, redirect=get_safe_redirect())
        else:
            return error('invalid flag: {} or secret: {}'.format(list(flag), list(secret)))
    else:
        fg = render_template('fg_catch_unicorn.html', redirect=get_safe_redirect())
    return fg


@app.route("/nice_try", methods=["GET"])
def nice_try():
    # import ipdb; ipdb.set_trace()
    return render_template_string('nice_try.html', redirect=get_safe_redirect())


if __name__ == '__main__':
    app.run()
