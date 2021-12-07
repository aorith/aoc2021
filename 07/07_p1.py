#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r") as f:
    data = [int(x.strip()) for x in f.readlines()[0].split(",")]

max_hrz = max(data)
min_hrz = min(data)

less_fuel = None
best_hrz_pos = None

for i in range(min_hrz, max_hrz + 1):
    fuel = 0
    for h in data:
        while h != i:
            if h > i:
                h -= 1
                fuel += 1
            elif h < i:
                h += 1
                fuel += 1
            if less_fuel is not None and fuel > less_fuel:
                break
        if less_fuel is not None and fuel > less_fuel:
            break
    if less_fuel is None or fuel < less_fuel:
        less_fuel = fuel
        best_hrz_pos = i

print(f"Pos: {best_hrz_pos}, Fuel: {less_fuel}")
