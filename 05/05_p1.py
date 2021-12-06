#!/usr/bin/env python3

import sys
import itertools

if len(sys.argv) < 2:
    sys.exit(1)

file = sys.argv[1]

with open(file, "r") as f:
    content = f.readlines()
    content = [n.strip() for n in content]

LEN = 0
for l in content:
    split = l.split("->")
    left = split[0]
    right = split[1]
    vals = left.split(",") + right.split(",")
    vals = [int(n) for n in vals]
    for n in vals:
        if n > LEN:
            LEN = n


def print_board(board):
    for idx, row in enumerate(board):
        row = [str(x) for x in row]
        print(idx, "".join(row))
    print()


board = []
for x in range(LEN+1):
    row = [0 for y in range(LEN + 1)]
    board.append(row)


points = []
for l in content:
    split = l.split("->")
    left = [int(x) for x in split[0].split(",")]
    right = [int(x) for x in split[1].split(",")]
    x1 = left[0]
    y1 = left[1]
    x2 = right[0]
    y2 = right[1]

    if x1 == x2:
        if y1 < y2:
            for i in range(y1, y2 + 1):
                points.append([i, x1])
        elif y1 > y2:
            for i in range(y2, y1 + 1):
                points.append([i, x1])
    elif y1 == y2:
        if x1 < x2:
            for i in range(x1, x2 + 1):
                points.append([y1, i])
        elif x1 > x2:
            for i in range(x2, x1 + 1):
                points.append([y1, i])


#points.sort()
#points = list(points for points, _ in itertools.groupby(points))

print(LEN)
print(len(content))
print(len(board))
for p in points:
    x = p[1]
    y = p[0]
    print(y, x)
    board[y][x] += 1


total = 0
for row in board:
    for n in row:
        if n > 1:
            total += 1

print(f"total: {total}")
