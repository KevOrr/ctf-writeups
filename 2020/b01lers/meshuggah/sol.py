#!/usr/bin/env python3

import itertools as it
import re
import subprocess
import time
from datetime import datetime
from typing import Generator, List

import pwn


def get_rng_sequence(seed: int, n: int) -> List[int]:
    p = subprocess.run(
        ['./rand', str(seed), str(n)],
        env={'LD_LIBRARY_PATH': '.'},
        capture_output=True,
        encoding='utf-8',
    )
    return list(map(int, p.stdout.strip().split('\n')))

def spiral_times(center: int) -> Generator[int, None, None]:
    yield center
    for i in it.count(1):
        yield center + i
        yield center - i

def next_sale(p: pwn.tube) -> int:
    pattern = re.compile(br'Meshuggah-(\d+)\n')
    s = p.recvregex(pattern)
    if (match := pattern.search(s)) and (sale := match.group(1)):
        return int(sale)
    else:
        raise ValueError('No match')

def find_seed(init: List[int], center: int) -> int:
    n = len(init)
    for seed in spiral_times(center):
        print(f'Checking seed {seed}...')
        if get_rng_sequence(seed, n) == init:
            return seed

    assert False  # unreachable

# p = pwn.process('./meshuggah')
p = pwn.remote('pwn.ctf.b01lers.com', 1003)

initial_sequence = [next_sale(p) for _ in range(3)]
print(f'Got first three random ints: {initial_sequence}')

seed = find_seed(initial_sequence, int(time.time()))
print(f'Found seed: {seed}')

for choice in get_rng_sequence(seed, 92 + 3)[3:]:
    p.sendline(str(choice))

print(p.recvline_startswith('pctf{').decode('utf-8'))
