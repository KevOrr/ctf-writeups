#!/usr/bin/env python3

import binascii
import base64
import itertools

key = b'eglafdsewafslfewamfeopwamfe'
encrypted = binascii.a2b_hex('5857342f555c2528182b55175e5f543a14540a0617394504380a0e52')

xored = [c1 ^ c2 for c1,c2 in itertools.zip_longest(map(int, key), map(int, encrypted), fillvalue=0)]
xored_str = bytes(bytearray(reversed(xored)))

print(base64.b64decode(xored_str).decode('ascii'))
