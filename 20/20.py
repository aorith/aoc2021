#!/usr/bin/env python3

import sys
from collections import Counter

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()

A = Counter()
for i, c in enumerate(data[0].strip()):
    if c == "#":
        A[i] = True
    else:
        A[i] = False

I = Counter()
input_img = [l.strip() for l in data[2:]]
for y in range(len(input_img)):
    for x in range(len(input_img[0])):
        if input_img[y][x] == "#":
            I[(y, x)] = True
        else:
            I[(y, x)] = False


def get_range(C: Counter) -> int:
    max_x, min_x = max([a[1] for a in C.keys()]), min([a[1] for a in C.keys()])
    max_y, min_y = max([a[0] for a in C.keys()]), min([a[0] for a in C.keys()])
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            yield (y, x)


def print_img(C: Counter):
    max_x, min_x = max([a[1] for a in C.keys()]), min([a[1] for a in C.keys()])
    max_y, min_y = max([a[0] for a in C.keys()]), min([a[0] for a in C.keys()])
    print()
    for y in range(min_y, max_y + 1):
        r = ""
        for x in range(min_x, max_x + 1):
            r += "#" if C[(y, x)] else "·"
        print(r)
    print()


def calculate_pixel_value(p: tuple, C: Counter, default: int = 0) -> int:
    binary = ""
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            y, x = p[0] + dy, p[1] + dx
            if (y, x) in C:
                binary += str(int(C[(y, x)]))
            else:
                binary += str(default)
    return A[int(binary, 2)]


def step(X, steps) -> Counter:
    for i in range(steps):
        N = Counter()
        for p in get_range(X):
            if A[0] == 1 and i % 2 != 0:
                N[p] = calculate_pixel_value(p, X, default=1)
            else:
                N[p] = calculate_pixel_value(p, X)

        X = N.copy()
    return X


print_img(I)

X = step(I, 2)

p1 = sum(X.values())
print(f"\nPart 1: {p1}")

X = step(I, 50)
p2 = sum(X.values())
print(f"\nPart 2: {p2}")
