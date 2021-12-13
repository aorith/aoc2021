#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()
    coords = [x.strip() for x in data if len(x) > 1 and not x.startswith("fold")]
    folds = [x.strip() for x in data if len(x) > 1 and x.startswith("fold")]

max_x = max(int(x.split(",")[0]) for x in coords)
min_x = min(int(x.split(",")[0]) for x in coords)
max_y = max(int(x.split(",")[1]) for x in coords)
min_y = min(int(x.split(",")[1]) for x in coords)

M = {}
for coord in coords:
    x, y = coord.split(",")
    M[(int(x), int(y))] = True


def print_dots():
    dots = []
    count = 0
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            try:
                if (x, y) in M:
                    line += "#"
                    count += 1
                else:
                    line += "."
            except KeyError:
                continue
        dots.append(line)

    for d in dots:
        print(d)
    print(f"\nCount: {count}\n")


for i, fold in enumerate(folds):
    fold = fold.split()[-1].split("=")
    fv = int(fold[1])
    if fold[0] == "y":
        max_y = fv - 1
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, (fv * 2) - y) in M:
                    M[(x, y)] = True
    else:
        assert fold[0] == "x"
        max_x = fv - 1
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if ((fv * 2) - x, y) in M:
                    M[(x, y)] = True
    if i == 0:  # Part 1
        print_dots()


print_dots()
