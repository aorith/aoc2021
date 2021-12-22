#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()[0].strip()

ta_x1 = int(data.split()[2].split(".")[0].split("=")[1])
ta_x2 = int(data.split()[2].split(".")[-1].split(",")[0])
ta_y1 = int(data.split()[-1].split(".")[0].split("=")[1])
ta_y2 = int(data.split()[-1].split(".")[-1])

max_ta = max(ta_x1, ta_x2, ta_y1, ta_y2)
min_ta = min(ta_x1, ta_x2, ta_y1, ta_y2)


def step(x, y, dx, dy):
    x += dx
    y += dy
    if dx != 0:
        dx += 1 if dx < 0 else -1
    dy -= 1
    # print(f"pos: {x},{y} - vel: {dx},{dy}, dist: {distance(x,y)}")
    return x, y, dx, dy


def distance(x, y):
    xd, yd = None, None
    if ta_x1 <= x <= ta_x2 and ta_y1 <= y <= ta_y2:
        return 0, 0
    elif ta_x1 <= x <= ta_x2:
        xd = 0
    elif ta_y1 <= y <= ta_y2:
        yd = 0

    if xd is None:
        if x < ta_x1:
            xd = ta_x1 - x
        else:
            xd = ta_x2 - x
    if yd is None:
        if y < ta_y1:
            yd = ta_y1 - y
        else:
            yd = ta_y2 - y
    return xd, yd


def calc(ix, iy):
    maxy = 0
    x, y, dx, dy = 0, 0, ix, iy
    while True:
        x, y, dx, dy = step(x, y, dx, dy)
        dist = distance(x, y)
        maxy = max(maxy, y)
        if dist[0] == 0 and dist[1] == 0:
            return maxy, (ix, iy)

        if ta_x1 > x and dx <= 0 or ta_y1 > y and dy <= 0:
            return None


result = [0, (0, 0)]
in_tgt = set()
for x in range(min_ta * 2, max_ta * 2):
    for y in range(min_ta * 2, max_ta * 2):
        output = calc(x, y)
        if not output:
            continue

        maxy, pos = output
        in_tgt.add(pos)
        if maxy > result[0]:
            result = [maxy, pos]
            print(result)

print(f"Part 1: {result[0]}")
print(f"Part 2: {len(in_tgt)}")
