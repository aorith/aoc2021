#!/usr/bin/env python3
from collections import Counter

import sys

with open(sys.argv[1], "r") as f:
    content = f.readlines()
    content = [n.replace("->", ",") for n in content]
    lines = [[int(x.strip()) for x in n.split(",")] for n in content]


def calcLine(x1, y1, x2, y2):
    # 3,4 -> 5,2
    dx = x2 - x1  # 2
    dy = y2 - y1  # -2
    sx = 0 if dx == 0 else (1 if dx > 0 else -1)
    sy = 0 if dy == 0 else (1 if dy > 0 else -1)

    for i in range(max(abs(dx), abs(dy)) + 1):  # 0,1,2
        yield x1 + i * sx, y1 + i * sy  # 3 + 0 * 1, 4 + 0 * -1 == 3,4


def result(diag=False):
    counter = Counter()
    for x1, y1, x2, y2 in lines:
        if diag or x1 == x2 or y1 == y2:
            for l in calcLine(x1, y1, x2, y2):
                counter[l] += 1
    return sum(x > 1 for x in counter.values())


print(f"P1: {result()}")
print(f"P2: {result(diag=True)}")
