#!/usr/bin/env python3

import sys
from itertools import permutations


with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()


def transform(point, ax, offset=(0, 0, 0)):
    assert len(point) == 3
    assert 0 <= ax < 48
    assert len(offset) == 3

    coord = list(point)
    for i, p in enumerate(permutations((0, 1, 2))):
        if i == ax // 8:
            coord = [coord[p[0]], coord[p[1]], coord[p[2]]]
            break

    signs = (
        1 if ax % 2 == 1 else -1,
        1 if ax // 2 % 2 == 1 else -1,
        1 if ax // 4 % 2 == 1 else -1,
    )
    for i in range(3):
        coord[i] *= signs[i]
        coord[i] += offset[i]

    return tuple(coord)


def compute_transforms(point1, point2):
    for ax in range(48):
        no_offset = transform(point1, ax)
        offset = []
        for i in range(3):
            offset.append(point2[i] - no_offset[i])
        yield ax, tuple(offset)


def find_valid_transform(ref_coords, coords):
    for ref_coord in ref_coords:
        for coord in coords:
            for ax, offset in compute_transforms(coord, ref_coord):
                # now we have a transformation of a coordinate to a reference
                # coordinate, let's see if this transformation yields 12 or more
                # matches ...
                matches = 0
                for coord2 in coords:
                    if transform(coord2, ax, offset) in ref_coords:
                        matches += 1
                        if matches == 12:
                            return ax, offset


scanners = []
coords = []
for l in data:
    if l.startswith("---"):
        coords = []
    elif len(l) > 1 and (l[0].isdigit() or l[1].isdigit()):
        l = l.strip().split(",")
        coords.append(tuple([int(v) for v in l]))
    else:
        scanners.append(coords)
scanners.append(coords)


for i in range(len(scanners)):
    print(f"[Scanner {i}, {len(scanners[i])} beacons.]")
    for c in scanners[i]:
        print(c)


ref_coords = set(scanners[0])
offsets = [None] * len(scanners)
offsets[0] = (0, 0, 0)
found = set()
while True:
    anything = False
    for i in range(len(scanners)):
        if i == 0 or i in found:
            continue

        t = find_valid_transform(ref_coords, scanners[i])
        if t is not None:
            ax, offset = t
            anything = True
            offsets[i] = offset
            found.add(i)
            print(f"Found match for {i} - ax:{ax}, offset:{offset}")
            for c in scanners[i]:
                good_coord = transform(c, ax, offset)
                if good_coord in ref_coords:
                    print(good_coord)
                ref_coords.add(good_coord)

    if len(found) == len(scanners) - 1:
        break
    if not anything:
        break

print(f"\nPart 1: {len(ref_coords)}.")


def distance(p1, p2):
    if p1 == p2:
        return 0
    d_x = abs(p1[0] - p2[0])
    d_y = abs(p1[1] - p2[1])
    d_z = abs(p1[2] - p2[2])
    return d_x + d_y + d_z


max_distance = 0
for c1 in offsets:
    for c2 in offsets:
        max_distance = max(distance(c1, c2), max_distance)

print(f"Part 2: {max_distance}.")
