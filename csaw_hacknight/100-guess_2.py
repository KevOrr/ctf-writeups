#!/usr/bin/env python3

import re, socket, time

def test(i):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('hn.csaw.io', 9001))
    s.recv(1024)

    s.send(str(i).encode('ascii') + b'\n')
    time.sleep(0.05)

    return s.recv(1024)

for i in range(1000):
    resp = test(i)
    print(resp.decode('ascii'), end='')
    
    msg = resp.split(b'\r\n')[1]
    if msg not in (b'kek'):
        break

