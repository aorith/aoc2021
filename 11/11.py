#!/usr/bin/env python3

import sys


with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()

data = [[int(y) for y in list(x.strip())] for x in data]


def reset_flashes():
    flashes = []
    for _ in range(len(data)):
        flashes.append([0] * len(data))
    return flashes


def get_neighbors(y, x):
    n = []
    if y - 1 >= 0:
        n.append([y - 1, x])  # up
        if x - 1 >= 0:
            n.append([y - 1, x - 1])  # up-left
        if x + 1 < len(data[0]):
            n.append([y - 1, x + 1])  # up-right
    if y + 1 < len(data):
        n.append([y + 1, x])  # down
        if x - 1 >= 0:
            n.append([y + 1, x - 1])  # down-left
        if x + 1 < len(data[0]):
            n.append([y + 1, x + 1])  # down-right

    if x - 1 >= 0:
        n.append([y, x - 1])  # left
    if x + 1 < len(data[0]):
        n.append([y, x + 1])  # right

    return n


def flash(flashes, data, neigh):
    if not neigh:
        return flashes, data

    for n in neigh:
        y, x = n
        if flashes[y][x] == 1:
            continue  # already flashed
        if data[y][x] <= 9:
            continue  # no need to flash

        flashes[y][x] = 1
        neighbors = [n2 for n2 in get_neighbors(y, x) if flashes[n2[0]][n2[1]] == 0]
        for n2 in neighbors:
            y2, x2 = n2
            data[y2][x2] += 1
        flashes, data = flash(flashes, data, neighbors)

    return flashes, data


def calc_step(data):
    flashes = reset_flashes()
    # increment all
    for y in range(len(data)):
        for x in range(len(data[0])):
            data[y][x] += 1

    # flash
    for y in range(len(data)):
        for x in range(len(data[0])):
            flashes, data = flash(flashes, data, [[y, x]])

    # count & reset energy
    step_flashes = 0
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] > 9:
                data[y][x] = 0
            if flashes[y][x] == 1:
                step_flashes += 1

    return data, step_flashes


total_flashes = 0
step = 0
while True:
    step += 1
    data, step_flashes = calc_step(data)
    total_flashes += step_flashes
    if step == 100:
        print(f"Part 1: {total_flashes}")

    # Part 2
    energy = 0
    for row in data:
        energy += sum(row)
    if energy == 0:  # all flashed in this step
        print(f"Part 2: {step}")
        break
