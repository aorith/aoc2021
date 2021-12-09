#!/usr/bin/env python3

import sys
from math import prod

with open(sys.argv[1], "r", encoding="utf-8") as f:
    matrix = []
    basin = []
    data = f.readlines()
    for row in data:
        matrix.append([int(x) for x in list(row.strip())])
        basin.append([0 for x in list(row.strip())])


def get_val(y, x):
    if x < 0 or y < 0 or y > len(data) - 1 or x > len(matrix[0]) - 1:
        return sys.maxsize
    return int(matrix[y][x])


def get_neighbors_coord(y, x):
    return (
        None if y - 1 < 0 else (y - 1, x),  # up
        None if y + 1 > len(data) - 1 else (y + 1, x),  # down
        None if x - 1 < 0 else (y, x - 1),  # left
        None if x + 1 > len(matrix[0]) - 1 else (y, x + 1),  # right
    )


def get_neighbors_val(y, x):
    return (
        get_val(y - 1, x),  # up
        get_val(y + 1, x),  # down
        get_val(y, x - 1),  # left
        get_val(y, x + 1),  # right
    )


def calc_basin(total, neigh):
    if not neigh:
        return total

    next_neigh = []
    for n in neigh:
        neighbors = get_neighbors_coord(*n)
        for coord in neighbors:
            if coord is None:
                continue
            y, x = coord
            if basin[y][x] != 0:
                continue
            if matrix[y][x] >= 9:
                basin[y][x] = 1
                continue

            basin[y][x] = 1
            total += 1
            next_neigh.append(coord)

    return calc_basin(total, next_neigh)


total_risk_level = 0
basin_sizes = []
for y in range(len(data)):
    for x in range(len(matrix[0])):

        value = int(matrix[y][x])
        up, down, left, right = get_neighbors_val(y, x)

        if value < up and value < down and value < left and value < right:
            # print(f"{y}/{x}: {value}: u:{up},d:{down},l:{left},r:{right}")
            total_risk_level += value + 1
            basin_value = calc_basin(0, [(y, x)])
            basin_sizes.append(basin_value)
            # print(f"{y}/{x}: {basin_value}")


print(f"Part 1: {total_risk_level}")

basin_sizes.sort()
basin_sizes.reverse()
print(f"Part 2: {prod(basin_sizes[0:3])}")
