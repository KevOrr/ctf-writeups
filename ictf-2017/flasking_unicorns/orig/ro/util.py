import contextlib
import os
import shutil
import tempfile
import random


@contextlib.contextmanager
def cd(newdir, cleanup=lambda: None):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
        cleanup()


@contextlib.contextmanager
def tempdir():
    dirpath = tempfile.mkdtemp()

    def cleanup():
        shutil.rmtree(dirpath)

    with cd(dirpath, cleanup):
        yield dirpath


def _fold(iterable, direction):
    firststage = []
    ordering = lambda v: v
    if direction == 'right':
        ordering = reversed
    elif direction == 'random':
        ordering = lambda array: random.sample(array, len(array))

    for v in ordering(iterable):
        firststage.append(lambda start, func: func(start, v))

    def start_val_stage(start_val):
        def func_stage(func):
            val = start_val
            for l in firststage:
                val = l(val, func)
            return val
        return func_stage
    return start_val_stage


def fold_left(iterable):
    return _fold(iterable, 'left')


def fold_right(iterable):
    return _fold(iterable, 'right')


def fold(iterable):
    return _fold(iterable, 'random')
