#!/usr/bin/env python
# -*- coding: utf-8 -*-

from timeit import timeit

py = timeit('fib(100)', number=1_000_000, setup='from fib_py import fib')
cy = timeit('fib(100)', number=1_000_000, setup='from fib_cy import fib')
px = timeit('fib(100)', number=1_000_000, setup='from fib_x import fib')

print('Python Puro ', py)
print('Cython ', cy)
print('Cython Puro', px)
print(f'{py/cy}')
print(f'{py/px}')