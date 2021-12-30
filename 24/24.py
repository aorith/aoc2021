#!/usr/bin/env python3

import sys
from itertools import product

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()

new_data = []
first = True
row = []
count = 0
for line in data:
    l = line.strip().split()
    cmd = l[0]

    if cmd == "inp":
        count += 1
        if first:
            first = False
            row.append(line.strip())
        else:
            new_data.append(row)
            row = [line.strip()]
    else:
        row.append(line.strip())

new_data.append(row)
data = new_data.copy()
new_data.clear()


def solve(W):
    # only track z
    z = 0
    ans = [0] * 14

    easy_idx = 0
    for i, d in enumerate(data):
        if d[4] == "div z 26":
            # w = (z%26) - ?
            # find the negative number
            for inst in d:
                inst = inst.split()
                cmd = inst[0]
                args = inst[1:]
                if cmd == "add" and args[0] == "x" and args[1].startswith("-"):
                    negative = int(args[1])
                    req = (z % 26) + negative
                    # if the value required is not between 1 and 9, it's not valid
                    if req < 1 or req > 9:
                        return False
                    z //= 26
                    ans[i] = req
        else:
            inc = int(d[-3].split()[-1])
            z = (26 * z) + W[easy_idx] + inc
            ans[i] = W[easy_idx]
            easy_idx += 1
    return ans


def magic(numbers):
    for w in numbers:
        r = solve(w)
        if r:
            return "".join(map(str, r))


undetermined_digits_max = product(range(9, 0, -1), repeat=7)
undetermined_digits_min = product(range(1, 10, 1), repeat=7)

print(f"Part 1: {magic(undetermined_digits_max)}")
print(f"Part 2: {magic(undetermined_digits_min)}")
