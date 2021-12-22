#!/usr/bin/env python3

import sys
from itertools import combinations

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = [x.strip() for x in f.readlines()]


def explode(string):
    """
    If any pair is nested inside four pairs, the leftmost such pair explodes.

    To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair (if any), and the pair's right value is added to the first regular number to the right of the exploding pair (if any). Exploding pairs will always consist of two regular numbers. Then, the entire exploding pair is replaced with the regular number 0.
    """

    def _explode(left, right, x, y):
        idx_number_left = []
        i = len(left) - 1
        found = False
        while i > 0:
            if left[i].isdigit():
                found = True
                idx_number_left.append(i)
            elif found:
                break
            i -= 1
        idx_number_left.reverse()

        idx_number_right = []
        i = 0
        found = False
        while i < len(right):
            if right[i].isdigit():
                found = True
                idx_number_right.append(i)
            elif found:
                break
            i += 1

        if idx_number_left:
            number = x + int("".join([left[x] for x in idx_number_left]))
            n_l = left[: idx_number_left[0]]
            n_r = left[idx_number_left[-1] + 1 :]
            left = f"{n_l}{number}{n_r}"

        if idx_number_right:
            number = y + int("".join([right[x] for x in idx_number_right]))
            n_l = right[: idx_number_right[0]]
            n_r = right[idx_number_right[-1] + 1 :]
            right = f"{n_l}{number}{n_r}"

        result = left + "0" + right
        return result

    level = 0
    for i, c in enumerate(string):
        if c == "[":
            level += 1
        elif c == "]":
            level -= 1
        elif c.isdigit():
            if level >= 5:
                di = 1
                while True:
                    if string[i + di] == "]":
                        # ok to explode
                        left = string[: i - 1]
                        right = string[i + di + 1 :]
                        x = int(string[i : i + di].split(",")[0])
                        y = int(string[i : i + di].split(",")[1])
                        return _explode(left, right, x, y)
                    elif string[i + di] == "[":
                        break
                    di += 1


def split(string):
    """
    If any regular number is 10 or greater, the leftmost such regular number splits.

    To split a regular number, replace it with a pair; the left element of the pair should be the regular number divided by two and rounded down, while the right element of the pair should be the regular number divided by two and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
    """

    for i, c in enumerate(string):
        if c.isdigit():
            if string[i + 1].isdigit():
                # we have a number >= 10
                n = c
                di = i + 1
                while string[di].isdigit():
                    n += string[di]
                    di += 1
                n_left = int(n) // 2
                n_right = int(n) // 2
                if n_left + n_right < int(n):
                    n_right += 1
                left = string[:i]
                right = string[di:]
                return f"{left}[{n_left},{n_right}]{right}"


def reduce(string):
    s = string
    while True:
        new_s = explode(s)
        if new_s is None:
            new_s = split(s)
            if new_s is None:
                if s != string:
                    print(s)
                return s
            else:
                s = new_s
        else:
            s = new_s


def add(s1, s2):
    s1 = reduce(s1)
    s2 = reduce(s2)
    return reduce(f"[{s1},{s2}]")


def magnitude(s):
    """
    To check whether it's the right answer, the snailfish teacher only checks the magnitude of the final sum. The magnitude of a pair is 3 times the magnitude of its left element plus 2 times the magnitude of its right element. The magnitude of a regular number is just that number.

    For example, the magnitude of [9,1] is 3*9 + 2*1 = 29; the magnitude of [1,9] is 3*1 + 2*9 = 21. Magnitude calculations are recursive: the magnitude of [[9,1],[1,9]] is 3*29 + 2*21 = 129.
    """
    if not "[" in s and not "," in s:
        return int(s)
    level = 0
    maxlevel = 0
    for c in s:
        if c == "[":
            level += 1
        elif c == "]":
            level -= 1
        maxlevel = max(level, maxlevel)

    level = 0
    for i, c in enumerate(s):
        if c == "[":
            level += 1
        elif c == "]":
            level -= 1

        if level == maxlevel:
            x, y = "", ""
            dx1 = i + 1
            dx2 = i + 1
            while s[dx2].isdigit():
                x += s[dx2]
                dx2 += 1
            dx2 -= 1
            assert s[dx2 + 1] == ","

            dy1 = dx2 + 2
            dy2 = dx2 + 2
            while s[dy2].isdigit():
                y += s[dy2]
                dy2 += 1
            dy2 -= 1

            left_n = int(s[dx1 : dx2 + 1]) * 3
            right_n = int(s[dy1 : dy2 + 1]) * 2
            number = left_n + right_n

            left = s[: dx1 - 1]
            right = s[dy2 + 2 :]
            result = left + str(number) + right
            return magnitude(result)


s = data[0]
for i, l in enumerate(data):
    if i == 0:
        continue
    s = add(s, l)

p1 = magnitude(s)

maxmag = 0
for s1, s2 in combinations(data, 2):
    s = add(s1, s2)
    maxmag = max(maxmag, magnitude(s))


print(f"\nPart 1: {p1}")
print(f"\nPart 2: {maxmag}")
