#!/usr/bin/env python3

import sys
import random

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()
    data = [r.split("|") for r in data]
    data = [[r[0].strip().split(), r[1].strip().split()] for r in data]


SEGMENTS = {
    #   a, b, c, d, e, f, g
    0: [1, 1, 1, 0, 1, 1, 1],
    1: [0, 0, 1, 0, 0, 1, 0],
    2: [1, 0, 1, 1, 1, 0, 1],
    3: [1, 0, 1, 1, 0, 1, 1],
    4: [0, 1, 1, 1, 0, 1, 0],
    5: [1, 1, 0, 1, 0, 1, 1],
    6: [1, 1, 0, 1, 1, 1, 1],
    7: [1, 0, 1, 0, 0, 1, 0],
    8: [1, 1, 1, 1, 1, 1, 1],
    9: [1, 1, 1, 1, 0, 1, 1],
}

DISPLAY = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
}

KNOWN = {1: "cf", 7: "acf", 4: "bcdf", 8: "abcdefg"}

BROKEN_DISPLAY = {
    "a": None,
    "b": None,
    "c": None,
    "d": None,
    "e": None,
    "f": None,
    "g": None,
}


def generate_broken_display():
    display = {}
    # values = []
    # for _ in range(7):
    #    values.append(random.randint(0, 6))
    values = [0, 1, 2, 3, 4, 5, 6]
    random.shuffle(values)
    letters = ["a", "b", "c", "d", "e", "f", "g"]
    random.shuffle(letters)
    for i, c in zip(values, letters):
        display[c] = i
    return display


def get_corresponding_num_for_segment(segment):
    for num, good_segment in SEGMENTS.items():
        if segment == good_segment:
            return num
    return None


def get_segment(signal, display):
    disp = [0] * 7
    for c in signal:
        disp[display.get(c)] = 1
    return disp


def get_unique_value(p):
    length = len(p)
    for k, v in KNOWN.items():
        if len(v) == length:
            return k


def get_letter_for_position(pos, display):
    for k, v in display.items():
        if v == pos:
            return k
    return None


def luck_is_random(signals, outputs):
    broken_display = BROKEN_DISPLAY.copy()
    letters = []  # appending here the letters resolved

    # POSITION 0 (a)
    # len=2     len=3
    # 1(cf) and 7(acf) gives 'a'

    # So, if 1 is 'gf' and 7 is 'bgf' the letter 'b' can only be at position 0 (a)

    # since the list of signals is sorted by length, I know their index:
    one = set(signals[0])
    seven = set(signals[1])

    letter = seven.difference(one).pop()
    if letter in letters:
        print("Oops", letters, 0)
    letters.append(letter)
    broken_display[letter] = 0

    # --- POSITION 3 (d)
    # Now, 0 and 8, give us 'd' position:
    # since the 0 is missing the 'd', so we need the difference again
    #
    #   aa    aa
    #  b  c  b  c
    #  b  c  b  c
    #   ..    dd
    #  e  f  e  f
    #  e  f  e  f
    #   gg    gg

    # But wait, we don't know which one is the 'zero', we know 'zero' has a
    # length of 6, but so does 'six', and 'nine':
    len_six = [s for s in signals if len(s) == 6]
    # now, the number 'six' doesn't have the segment 'c' and we know
    # that it's present in 'seven' we also know that 'zero' and 'nine' have
    # all the segments that 7 has, so we can rule 'six' out:
    filtered = [p for p in len_six if all((c in list(p) for c in list(seven)))]

    # Ok, now we should have 'zero' and 'nine' in 'len_six'.
    # we can do something similar to discard 'nine':
    # we know that 'nine' has all the segments that 'four' has, but 'zero' is
    # missing the 'd' segment.
    four = signals[2]
    zero = set([p for p in filtered if any((c not in list(p) for c in list(four)))][0])

    # Ok, we have 'zero' and 'eigth'
    eigth = [s for s in signals if len(s) == 7]
    eigth = set(eigth[0])

    # Get the letter missing in 0, it will be the position 3 (d)
    letter = eigth.difference(zero).pop()
    if letter in letters:
        print("Oops", letters, 3)
    letters.append(letter)
    broken_display[letter] = 3

    # Ok, now we have the letters for the segments 'a' and 'd'

    # --- POSITION 1 (b)
    # we can resolve the position 'b' now, since we have 'd' and 'one' contains
    # the segments for 'c' and 'f', so let's remove those from 'four' to get 'b'

    four_letters = list(four)
    letter = [c for c in four_letters if c not in list(one) + letters][0]
    if letter in letters:
        print("Oops", letters, 1)
    letters.append(letter)
    broken_display[letter] = 1

    # We have 'a' 'b' and 'd'

    # --- POSITION 6 (g)

    # We'll do something similar for the segment 'g'. The number 'five' has
    # the segments for 'a', 'b', 'd', 'f' and 'g'.
    # 'one' has 'c' and 'f', and the rest should be on the resolved letters list

    # We need to figure out the number 'five', which has a length of 5.
    # numbers with length 5: 'two', 'three' and 'five'
    len_five = [s for s in signals if len(s) == 5]
    # 'two' and 'three' don't have the letter 'b', but 'five' does

    five = None
    for pattern in len_five:
        # the letter 'b' position is 1 and we have it already resolved:
        if get_letter_for_position(1, broken_display) in list(pattern):
            five = pattern
            break

    # Ok, we know the pattern of 'five', let's resolve the letter 'g':
    five_letters = list(five)
    letter = [c for c in five_letters if c not in letters + list(one)][0]
    if letter in letters:
        print("Oops", letters, 6)
    letters.append(letter)
    broken_display[letter] = 6

    # --- POSITION 5 (f)

    # we can leverage the number 'five' too to get the letter 'f' we have all
    # from 'five' except 'f' so it is easy:
    five_letters = list(five)
    letter = [c for c in five_letters if c not in letters][0]
    if letter in letters:
        print("Oops", letters, 5)
    letters.append(letter)
    broken_display[letter] = 5

    # --- POSITION 2 (c)

    #          0   1   3   5   6
    # We have 'a' 'b' 'd' 'f' 'g', we can get 'c' from 'one'

    letter = [c for c in list(one) if c not in letters][0]
    if letter in letters:
        print("Oops", letters, 2)
    letters.append(letter)
    broken_display[letter] = 2

    # --- POSITION 4 (e)

    # Ok, just missing this letter, let's get it from eigth
    letter = [c for c in list(eigth) if c not in letters][0]
    if letter in letters:
        print("Oops", letters, 4)
    letters.append(letter)
    broken_display[letter] = 4

    # return the fixed display!
    return broken_display


counter = 0
total = 0
for row in data:
    signals = [x.strip() for x in sorted(row[0], key=len)]
    outputs = [x.strip() for x in row[1]]
    for o in outputs:
        if get_unique_value(o) is not None:
            counter += 1

    decoded_display = luck_is_random(signals, outputs)
    txt_value = ""
    for o in outputs:
        segment = get_segment(o, decoded_display)
        value = get_corresponding_num_for_segment(segment)
        if value is None:
            print(f"{o}: {value} !!!")
            continue
        txt_value += str(value)

    total += int(txt_value)

print(f"Part 1: {counter}")
print(f"Part 2: {total}")
