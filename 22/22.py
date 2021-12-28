#!/usr/bin/env python3

import sys
from collections import Counter

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()


def parse_step(line, allowed=(-50, 50)):
    line = line.strip()
    _type = 1 if line.split()[0] == "on" else 0
    line = line.split()[1]

    xr = line.split(",")[0].split("=")[1]
    x1 = int(xr.split("..")[0])
    x2 = int(xr.split("..")[1])

    yr = line.split(",")[1].split("=")[1]
    y1 = int(yr.split("..")[0])
    y2 = int(yr.split("..")[1])

    zr = line.split(",")[2].split("=")[1]
    z1 = int(zr.split("..")[0])
    z2 = int(zr.split("..")[1])

    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)
    z1, z2 = min(z1, z2), max(z1, z2)

    if allowed is not None:
        X1, X2 = min(allowed[1], max(x1, allowed[0])), max(
            allowed[0], min(allowed[1], x2)
        )
        Y1, Y2 = min(allowed[1], max(y1, allowed[0])), max(
            allowed[0], min(allowed[1], y2)
        )
        Z1, Z2 = min(allowed[1], max(z1, allowed[0])), max(
            allowed[0], min(allowed[1], z2)
        )

        if (x1 < allowed[0] and x2 < allowed[0]) or (
            x1 > allowed[1] and x2 > allowed[1]
        ):
            # return null range
            X1, X2 = 0, -1
        if (y1 < allowed[0] and y2 < allowed[0]) or (
            y1 > allowed[1] and y2 > allowed[1]
        ):
            Y1, Y2 = 0, -1
        if (z1 < allowed[0] and z2 < allowed[0]) or (
            z1 > allowed[1] and z2 > allowed[1]
        ):
            Z1, Z2 = 0, -1
    else:
        X1, X2 = x1, x2
        Y1, Y2 = y1, y2
        Z1, Z2 = z1, z2

    return (
        _type,
        range(X1, X2 + 1),
        range(Y1, Y2 + 1),
        range(Z1, Z2 + 1),
    )


def magic(part=1):
    C = set()
    for step, l in enumerate(data):
        _type, xr, yr, zr = parse_step(l, allowed=(-50, 50) if part == 1 else None)
        print(f"Working on step {step} ({_type}): {xr}, {yr}, {zr} ...")
        for x in xr:
            for y in yr:
                for z in zr:
                    if _type == 0:
                        C.discard((x, y, z))
                    else:
                        C.add((x, y, z))

    print(f"Part {part}: {len(C)}")


def size(cube):
    s = 1
    for a in cube:
        s *= abs(a[1] - a[0]) + 1
    return s


def intersection(cube1, cube2):
    ans = []
    for ax1, ax2 in zip(cube1, cube2):
        if ax1[1] < ax2[0] or ax2[1] < ax1[0]:
            return None

        ax = (max(ax1[0], ax2[0]), min(ax1[1], ax2[1]))
        ans.append(ax)

    return tuple(ans)


def magic2(part=1):
    cubes = Counter()

    for step, l in enumerate(data):
        _type, xr, yr, zr = parse_step(l, allowed=(-50, 50) if part == 1 else None)
        print(
            f"{'+ Add' if _type == 1 else '- Del'} => Step {step}: {xr}, {yr}, {zr} ..."
        )
        if not list(xr) or not list(yr) or not list(zr):
            continue

        cube = ((min(xr), max(xr)), (min(yr), max(yr)), (min(zr), max(zr)))

        new_cubes = Counter()
        for o_c in cubes:
            i_c = intersection(cube, o_c)
            if i_c is None:
                continue

            # substract other cube count
            new_cubes[i_c] -= cubes[o_c]

        if _type == 1:
            new_cubes[cube] += 1

        diff = 0
        for c in new_cubes:
            diff += size(c) * new_cubes[c]
            cubes[c] += new_cubes[c]
        print(f"    * diff: {diff}")

    ans = 0
    for c in cubes:
        ans += size(c) * cubes[c]
    print(f"Part {part}: {ans}")


magic2(part=1)
magic2(part=2)
