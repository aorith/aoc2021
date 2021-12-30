#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r", encoding="utf-8") as f:
    lines = f.readlines()
    data = [r.strip() for r in lines]

new_data = []
for r in data:
    new_data.append(list(r))
data = new_data.copy()
new_data.clear()


def show(data):
    for r in data:
        print("".join(r))
    print()


def move(data, moves):
    new_data = data.copy()
    for _from, _to in moves:
        y1, x1 = _from
        y2, x2 = _to
        v = new_data[y1][x1]
        new_data[y1][x1] = "."
        new_data[y2][x2] = v
    return new_data


def step(data):
    H = len(data)
    W = len(data[0])
    # '>' first
    moved = False
    moves = []
    for y, r in enumerate(data):
        for x, c in enumerate(r):
            if c == ">":
                nx = x + 1
                if nx >= W:
                    nx = 0
                if data[y][nx] == ".":
                    moves.append(((y, x), (y, nx)))

    if moves:
        data = move(data, moves)
        moved = True

    # 'v' now
    moves = []
    for y, r in enumerate(data):
        for x, c in enumerate(r):
            if c == "v":
                ny = y + 1
                if ny >= H:
                    ny = 0
                if data[ny][x] == ".":
                    moves.append(((y, x), (ny, x)))
    if moves:
        data = move(data, moves)
        moved = True
    return moved, data


count = 0
moved = True
while moved:
    moved, data = step(data)
    count += 1

print(f"Part 1: {count}")
