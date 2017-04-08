#!/usr/bin/env python

import requests

with open('shattered-1.pdf', 'rb') as f:
    shattered1 = f.read()

with open('shattered-2.pdf', 'rb') as f:
    shattered2 = f.read()

r = requests.get('http://54.202.82.13/', params={'name': shattered1, 'password': shattered2})
print r.text
