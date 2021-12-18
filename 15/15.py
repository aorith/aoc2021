#!/usr/bin/python3

import sys
import heapq

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()
    data = [[int(x) for x in list(r.strip())] for r in data]


NEIGH = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def calc_min(size=1):
    ox, oy = len(data[0]), len(data)
    mx, my = len(data[0]) * size, len(data) * size
    M = [[None] * mx for _ in range(my)]
    for x in range(mx):
        for y in range(oy):
            for i in range(size):
                if x == 0:
                    val = data[x][y] + i
                else:
                    _i = x // ox
                    val = data[x - _i * ox][y] + i + _i

                while val > 9:
                    val -= 9
                M[x][y + oy * i] = val

    R = [[-1] * mx for _ in range(my)]
    Q = [(0, 0, 0)]
    while Q:
        (risk, x, y) = heapq.heappop(Q)
        for dx, dy in NEIGH:
            X, Y = dx + x, dy + y
            if 0 <= X < mx and 0 <= Y < my and R[X][Y] == -1:
                R[X][Y] = risk + M[X][Y]
                heapq.heappush(Q, (R[X][Y], X, Y))
    return R[-1][-1]


print(f"Part 1: {calc_min()}")
print(f"Part 2: {calc_min(5)}")
