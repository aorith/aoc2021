#!/usr/bin/env python3

import sys
from collections import Counter

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()

p1 = int(data[0].split()[4])
p2 = int(data[1].split()[4])


class DeterministicDice:
    last_roll = 0
    n_rolls = 0

    def roll(self):
        if self.last_roll == 100:
            self.last_roll = 0
        self.last_roll += 1
        self.n_rolls += 1
        return self.last_roll

    def multiple_rolls(self, count):
        total = 0
        for _ in range(count):
            total += self.roll()
        return total


def move(start, roll):
    for _ in range(roll):
        start += 1
        if start == 11:
            start = 1
    return start


p1_points = 0
p2_points = 0
turn = True
dice = DeterministicDice()
while True:
    if turn:
        p1 = move(p1, dice.multiple_rolls(3))
        p1_points += p1
    else:
        p2 = move(p2, dice.multiple_rolls(3))
        p2_points += p2

    if p1_points >= 1000 or p2_points >= 1000:
        break
    turn = not turn

if p1_points > p2_points:
    print(f"P1 wins: {p1_points}")
    print(f"Part 1: {p2_points * dice.n_rolls}")
else:
    print(f"P2 wins: {p2_points}")
    print(f"Part 1: {p1_points * dice.n_rolls}")


# WHAT
"""
the universe splits into multiple copies, one copy for each possible outcome of the die. In this case, rolling the die always splits the universe into three copies: one where the outcome of the roll was 1, one where it was 2, and one where it was 3.
"""
MAX_SCORE = 21


W = {}


def game(p1, s1, p2, s2, turn):
    turn = 1 if turn == 0 else 0
    if s1 >= MAX_SCORE:
        return (1, 0)
    if s2 >= MAX_SCORE:
        return (0, 1)
    if (p1, s1, p2, s2, turn) in W:
        return W[(p1, s1, p2, s2, turn)]

    result = [0, 0]
    for r1 in (1, 2, 3):
        for r2 in (1, 2, 3):
            for r3 in (1, 2, 3):
                r = r1 + r2 + r3
                if turn == 1:
                    new_p1 = move(p1, r)
                    new_s1 = s1 + new_p1
                    w1, w2 = game(new_p1, new_s1, p2, s2, turn)
                else:
                    new_p2 = move(p2, r)
                    new_s2 = s2 + new_p2
                    w1, w2 = game(p1, s1, new_p2, new_s2, turn)

                result = [result[0] + w1, result[1] + w2]

    W[(p1, s1, p2, s2, turn)] = result
    return result


p1 = int(data[0].split()[4])
p2 = int(data[1].split()[4])
s1 = 0
s2 = 0
print("Part 2:", max(game(p1, s1, p2, s2, 0)))
