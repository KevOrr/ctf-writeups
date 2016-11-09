#!/usr/bin/env python3

import re
from Crypto.PublicKey import RSA

with open('trumpkey') as f:
    trumpkey = f.read()

modulus = int(re.search('e (\d+)', trumpkey, ).groups()[0])
exponent = int(re.search('N (\d+)', trumpkey, ).groups()[0])

pubkey = RSA.construct((modulus, exponent))

with open('key.pem', 'wb') as f:
    f.write(pubkey.exportKey('PEM') + b'\n')

# with open('key.der', 'wb') as f:
#     f.write(pubkey.exportKey('DER') + b'\n')

