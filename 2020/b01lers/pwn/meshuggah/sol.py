#!/usr/bin/env python3

import itertools as it
import re
import subprocess
import time
from datetime import datetime
from typing import Generator, List

import pwn


def get_rng_sequence(seed: int, n: int, program: str = './rand') -> List[int]:
    p = subprocess.run([program, str(seed), str(n)], capture_output=True, encoding='utf-8')
    return list(map(int, p.stdout.strip().split('\n')))

def spiral_times(center: int) -> Generator[int, None, None]:
    yield center
    for i in it.count(1):
        yield center + i
        yield center - i

def next_sale(p: pwn.tube) -> int:
    pattern = re.compile(br'Meshuggah-(\d+)\n')
    s = p.recvregex(pattern)
    if ((match := pattern.search(s)) and (sale := match.group(1))):
        return int(sale)
    else:
        raise ValueError('No match')

def find_seed(init: List[int], center: int, verbose = False) -> int:
    n = len(init)
    earliest = latest = center
    for i, t in enumerate(spiral_times(center)):
        if get_rng_sequence(t, n) == init:
            return t

        if verbose:
            earliest = min(earliest, t)
            latest = max(latest, t)
            fmt = lambda t: datetime.fromtimestamp(t).strftime('%H:%M:%S')
            print(f'Searched {i} seeds from {fmt(earliest)} to {fmt(latest)}')

    assert False # unreachable

# p = pwn.process('./meshuggah')
p = pwn.remote('pwn.ctf.b01lers.com', 1003)

initial_sequence = [next_sale(p) for _ in range(3)]
print(f'Got first three random ints: {initial_sequence}')

seed = find_seed(initial_sequence, int(time.time()), verbose=True)
print(f'Found seed: {seed}')

for choice in get_rng_sequence(seed, 100)[3:]:
    p.sendline(str(choice))

print(p.recvline_startswith('pctf{').decode('utf-8'))
