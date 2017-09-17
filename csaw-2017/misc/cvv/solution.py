#!/usr/bin/env python2

import random
import re
import sys

from pwn import *

class MyRemote(remote):
    def __init__(self, *args, **kwargs):
        super(MyRemote, self).__init__(*args, **kwargs)
        self._mirror_streams = True

    def recv_raw(self, *args, **kwargs):
        data = super(MyRemote, self).recv_raw(*args, **kwargs)
        if self._mirror_streams:
            sys.stdout.write(data)
        return data

    def send_raw(self, data, *args, **kwargs):
        super(MyRemote, self).send_raw(data, *args, **kwargs)
        if self._mirror_streams:
            sys.stdout.write(data)

    def interactive(self, *args, **kwargs):
        self._mirror_streams = False
        super(MyRemote, self).interactive(*args, **kwargs)

    def stream(self, *args, **kwargs):
        self._mirror_streams = False
        super(MyRemote, self).interactive(*args, **kwargs)

ISSUERS = {
    'visa': [[4]],
    'mastercard': [[5, 1], [5, 2], [5, 3], [5, 4], [5, 5]],
    'american express': [[3, 7]],
    'discover': [[6, 0, 1, 1], [6, 5]]
}

ACCOUNT_LENGTHS = {
    'visa': 9,
    'mastercard': 9,
    'american express': 8,
    'discover': 9
}


def sum_digits(n):
    total = 0
    while n:
        n, rem = divmod(n, 10)
        total += rem
    return total


def generate_from_prefix(prefix, acct_length=9):
    remaining = 6 - len(prefix) + acct_length
    with_acct = prefix + [random.randint(0, 9) for i in range(remaining)]

    luhn = 0
    for i, digit in enumerate(reversed(with_acct)):
        multiplier = 1 if i % 2 else 2
        luhn += sum_digits(digit * multiplier)

    check_digit = (10 - luhn % 10) % 10
    return ''.join(map(str, with_acct + [check_digit]))

def generate_from_suffix(suffix, acct_length=9):

    return ''.join(map(str, candidate))


def generate_from_issuer(issuer):
    return generate_from_prefix(random.choice(ISSUERS[issuer]), ACCOUNT_LENGTHS[issuer])


def main():
    r = MyRemote('misc.chal.csaw.io', 8308)
    prefix_pattern = re.compile('I need a new card that starts with (\d+)!')
    checkdigit_pattern = re.compile('I need a new card which ends with (\d)!')
    issuer_pattern = re.compile('I need a new ([^!]+)!')

    while True:
        line = r.recvline().strip()
        prefix_match = re.match(prefix_pattern, line)
        checkdigit_match = re.match(checkdigit_pattern, line)
        issuer_match = re.match(issuer_pattern, line)

        if prefix_match:
            r.sendline(generate_from_prefix(map(int, prefix_match.group(1))))
        elif checkdigit_match:
            r.sendline(generate_from_checkdigit(int(checkdigit_match.group(1))))
        elif issuer_match:
            r.sendline(generate_from_issuer(issuer_match.group(1).lower()))
        elif line:
            break

        if r.recvline().strip() != 'Thanks!':
            break

    r.interactive()


if __name__ == '__main__':
    main()
