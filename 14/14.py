#!/usr/bin/env python3

import sys
from collections import Counter

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()
    template = list(data[0].strip())
    pairs = [
        (x.split("->")[0].strip(), x.split("->")[1].strip()) for x in data if "->" in x
    ]


C1 = Counter()
F = Counter()
for i in range(len(template) - 1):
    F[template[i]] += 1
    C1[template[i] + template[i + 1]] += 1
F[template[len(template) - 1]] += 1

C2 = C1
for step in range(40):
    F = Counter()
    C2 = Counter()
    for k in C1:
        found = False
        for p in pairs:
            if k == p[0]:
                found = True
                C2[k[0] + p[1]] += C1[k]
                C2[p[1] + k[1]] += C1[k]
                F[k[0]] += C1[k]
                F[p[1]] += C1[k]
                break

        if not found:
            C2[k] += C1[k]
            F[k[0]] += C1[k]

    # the last letter was left
    F[list(C1)[-1][1]] += C1[list(C1)[-1]]

    C1 = C2
    if step in [9, 39]:
        mx = max(F.values())
        mn = min(F.values())

        print(f"Part {1 if step == 9 else 2}: {mx - mn}")
