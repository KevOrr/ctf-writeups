#!/usr/bin/env python

from pwn import *

r = remote('54.202.2.54', 9876)

def try_commands():
    commands = (
        'ls', 'ls -l', 'ls -al', 'cat', 'tail', 'head', 'whoami', 'id', 'hostname', 'time',
        'echo', 'dd', 'gzip', 'tar', 'mv', 'cp', 'touch', 'mkdir', 'mktemp', 'sh', 'man',
        'vi', 'nano', ''
    )

    for command in commands:
        signature = get_sig(command)
        print command, signature if signature else 'blocked'

def get_sig(command):
    r.recvuntil('>_ ')
    r.sendline('1')
    r.recvuntil('>_ ')
    r.sendline(command)
    if 'signature' in r.recvline():
        signature = r.recvline().strip()
        return signature
    return None


def run_command(command, signature):
    r.recvuntil('>_ ')
    r.sendline('2')
    r.recvuntil('>_ ')
    r.sendline(command)
    r.recvuntil('>_ ')
    r.sendline(signature)
    r.interactive()

try_commands()

command = 'id'
run_command(command, get_sig(command))
