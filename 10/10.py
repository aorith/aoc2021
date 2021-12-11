#!/usr/bin/env python3

import sys

OPEN = ["(", "[", "{", "<"]
CLOSE = [")", "]", "}", ">"]
POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
POINTS2 = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()

data = [x.strip() for x in data]


def get_pair_for_opener(open_char):
    if open_char == OPEN[0]:
        return CLOSE[0]
    if open_char == OPEN[1]:
        return CLOSE[1]
    if open_char == OPEN[2]:
        return CLOSE[2]
    if open_char == OPEN[3]:
        return CLOSE[3]


illegals = []
scores = []

for line in data:
    openers = []
    closers = []
    for c in list(line):
        if c in OPEN:
            openers.append(c)
            closers.append(get_pair_for_opener(c))
        elif c in CLOSE:
            if not closers:
                # corrupted line
                illegals.append(c)
                closers = []
                break
            expected = closers.pop()
            if c == expected:
                _ = openers.pop()
            else:
                # corrupted line
                illegals.append(c)
                closers = []
                break

    # Part 2
    if closers:
        # incomplete line
        points = 0
        closers.reverse()
        for ch in closers:
            points = (points * 5) + POINTS2[ch]
        scores.append(points)


points = 0
for c in illegals:
    points += POINTS[c]
print(f"Part 1: {points}")

scores.sort()
points = scores[len(scores) // 2]
print(f"Part 2: {points}")
