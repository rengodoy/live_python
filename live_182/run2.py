#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from fib_cy import fib

numeros = [randint(0, 93) for _ in range(1_000_000) ]

for n in numeros:
    fib(n)
