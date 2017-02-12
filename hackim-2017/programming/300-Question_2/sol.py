#!/usr/bin/env python2.7

from pwn import *

urand = open('/dev/urandom')

while True:
    r = remote('52.90.9.177', 33333)
    r.recvuntil('Send in your unique signature from unique countries \n')
    r.send(urand.read(16).hex()[2:] + '\n')
