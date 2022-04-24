#!/usr/bin/env python3
from sys import argv
import random
for _ in range(int(argv[1])):
     x = random.uniform(-10000,10000)
     y = random.uniform(-10000,10000)
     print(x, ", ", y)