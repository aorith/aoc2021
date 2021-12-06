#!/usr/bin/env python3

import sys

days = 80

file = sys.argv[1]
with open(file, "r") as f:
    data = [int(x.strip()) for x in f.readlines()[0].split(",")]

def compute_day(d):
    new = []
    data = []
    for x in d:
        if x == 0:
            data.append(6)
            new.append(8)
        else:
            data.append(x-1)
    return data + new

for _ in range(days):
    data = compute_day(data)

print(len(data))
