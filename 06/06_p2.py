#!/usr/bin/env python3

import sys

days = 256
timers = 9


class Fishpool:
    def __init__(self, initial, timers=9):
        self.pool = {}
        self.timers = timers
        self.set_pool(initial)

    def set_pool(self, initial):
        for x in range(self.timers):
            self.pool[x] = 0
        for x in initial:
            self.pool[x] += 1

    def compute_day(self):
        new_pool = {}
        new_borns = 0
        for timer in range(self.timers):
            val = self.pool.get(timer, 0)
            if timer == 0:
                new_pool[6] = new_pool.get(6, 0) + val
                new_borns = val
            else:
                new_pool[timer - 1] = new_pool.get(timer - 1, 0) + val

        self.pool = new_pool.copy()
        self.pool[8] = new_borns

    def get_total(self):
        return sum(self.pool.values())


file = sys.argv[1]
with open(file, "r") as f:
    data = [int(x.strip()) for x in f.readlines()[0].split(",")]

fishpool = Fishpool(data, timers)
for day in range(days):
    fishpool.compute_day()

print(fishpool.get_total())
