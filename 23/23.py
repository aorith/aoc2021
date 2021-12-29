#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()

PIECES = ["A", "B", "C", "D"]
DOORS = {"A": 2, "B": 4, "C": 6, "D": 8}
COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}

# Part 1 (by hand):
#  20
#  6
#  30
#  200
#  70
#  9000
#  6
#  5000
#  500
#  700
#  3
#  3
#  = 15538


class State:
    score: int = 0
    H: list
    A: list
    B: list
    C: list
    D: list

    def complete(self) -> bool:
        W = {"A": self.A, "B": self.B, "C": self.C, "D": self.D}
        for k, v in W.items():
            if any(x != k for x in v):
                return False

        return True


def init_state(data, part) -> State:
    burrow = []
    length = None
    for i, r in enumerate(data):
        r = list(r.strip())
        if i == 0:
            length = len(r)
        else:
            assert length is not None
            while len(r) != length:
                r.insert(0, "#")
                r.append("#")
        burrow.append(r)

    if part == 2:
        """
        ###D#C#B#A###
        ###D#B#A#C###
        """
        burrow.insert(3, "###D#B#A#C###")
        burrow.insert(3, "###D#C#B#A###")

    H = burrow[1][1:-1]
    A = [burrow[i][3] for i in range(2, len(burrow) - 1)]
    B = [burrow[i][5] for i in range(2, len(burrow) - 1)]
    C = [burrow[i][7] for i in range(2, len(burrow) - 1)]
    D = [burrow[i][9] for i in range(2, len(burrow) - 1)]
    s = State()
    s.H = H
    s.A = A
    s.B = B
    s.C = C
    s.D = D
    return s


def copy_state(s: State) -> State:
    new_s = State()
    score = s.score
    new_s.H = s.H.copy()
    new_s.A = s.A.copy()
    new_s.B = s.B.copy()
    new_s.C = s.C.copy()
    new_s.D = s.D.copy()
    new_s.score = score
    return new_s


def moves(s: State) -> list:
    moves = []

    room_map = {
        "A": s.A,
        "B": s.B,
        "C": s.C,
        "D": s.D,
    }

    # hall pieces
    for i, p in enumerate(s.H):
        if p not in PIECES:
            continue

        # Into a room
        door_type = p
        door_idx = DOORS[door_type]
        if any(
            x not in [p, "."] for x in room_map[door_type]
        ):  # incorrect piece inside of the room
            continue

        if door_idx > i:
            # move to the right
            sign = 1
        else:
            # move to the left
            sign = -1

        hallway_free = True
        count = 1
        while i + (count * sign) != door_idx:
            if s.H[i + (count * sign)] in PIECES:
                hallway_free = False
                break
            count += 1

        if not hallway_free:
            continue

        hallway_steps = count

        last_free_idx = -1
        for ridx, rp in enumerate(room_map[door_type]):
            if rp == ".":
                last_free_idx = ridx
            else:
                break

        if last_free_idx != -1:
            total_steps = hallway_steps + last_free_idx + 1
            moves.append(("H", i, total_steps, door_type, last_free_idx))

    # Room moves
    for room_type, room in room_map.items():
        for i, p in enumerate(room):
            if p not in PIECES:
                continue

            # if the piece matches the room_type...
            if p == room_type:
                if len(room) == (i + 1) and p == room_type:  # last piece
                    continue
                if all(x == p for x in room):  # all pieces in the room are the same
                    continue

            # if we're here, get out of the room even if it's the correct one
            # since there must be an incorrect piece inside
            allowed_hallway_moves = []
            steps_to_door = i + 1

            # are there pieces blocking the door?
            blocked = False
            if i != 0:
                to_door_idx = i
                while to_door_idx != 0:
                    to_door_idx -= 1
                    if room[to_door_idx] in PIECES:
                        blocked = True
                        break
            if blocked:
                continue

            initial_idx = DOORS[room_type]
            for di in [-1, 1]:
                count = 1
                while 0 <= initial_idx + (count * di) < len(s.H):
                    cell_piece = s.H[initial_idx + (count * di)]
                    if cell_piece in PIECES:
                        break
                    if cell_piece == ".":
                        if initial_idx + (count * di) not in list(DOORS.values()):
                            allowed_hallway_moves.append(
                                (
                                    steps_to_door + count,
                                    initial_idx + (count * di),
                                )
                            )
                    count += 1

            for steps, final_idx in allowed_hallway_moves:
                moves.append((room_type, i, steps, "H", final_idx))

    return moves


def calculate(s, move) -> State:
    new_s = copy_state(s)
    full_map = {
        "A": new_s.A,
        "B": new_s.B,
        "C": new_s.C,
        "D": new_s.D,
        "H": new_s.H,
    }
    orig = move[0]
    orig_pos = move[1]
    steps = move[2]
    dest = move[3]
    dest_pos = move[4]

    piece = full_map[orig][orig_pos]
    cost = COSTS[piece] * steps

    # print(
    #  f"Moving piece {piece}, from {orig}:{orig_pos}, to {dest}:{dest_pos} using {steps} steps. Cost:{cost}"
    # )
    # show(new_s)

    # add score
    new_s.score += cost

    # reset
    if orig == "A":
        new_s.A[orig_pos] = "."
    elif orig == "B":
        new_s.B[orig_pos] = "."
    elif orig == "C":
        new_s.C[orig_pos] = "."
    elif orig == "D":
        new_s.D[orig_pos] = "."
    elif orig == "H":
        new_s.H[orig_pos] = "."
    else:
        assert False

    # move
    if dest == "A":
        new_s.A[dest_pos] = piece
    elif dest == "B":
        new_s.B[dest_pos] = piece
    elif dest == "C":
        new_s.C[dest_pos] = piece
    elif dest == "D":
        new_s.D[dest_pos] = piece
    elif dest == "H":
        new_s.H[dest_pos] = piece
    else:
        assert False

    # show(new_s)
    # print("-----------------------------")
    return new_s


def magic(s: State, score):
    states = []
    for move in moves(s):
        new_s = calculate(s, move)
        if new_s.complete():
            score = min(score, new_s.score)
            print(f"Score: {score}")
        elif new_s.score > score:
            continue
        else:
            states.append(new_s)

    return score, states


def show(s: State) -> None:
    print(f"Score: {s.score}")
    print("#" * 13)
    print(f"#{''.join(s.H)}#")
    for i in range(len(s.A)):
        print(f"###{s.A[i]}#{s.B[i]}#{s.C[i]}#{s.D[i]}###")
    print("#" * 13)
    print()


def run(part=1):
    score = 1e7
    s = None
    states = []
    seen = set()
    while True:
        if s is None:
            states.append(init_state(data, part))
            all_moves = moves(states[0])
        if not states:
            break

        new_states = []
        for s in states:
            if (
                s.score,
                tuple(s.A),
                tuple(s.B),
                tuple(s.C),
                tuple(s.D),
                tuple(s.H),
            ) in seen:
                continue

            new_score, res_states = magic(s, score)
            new_states = new_states + res_states

            seen.add(
                (s.score, tuple(s.A), tuple(s.B), tuple(s.C), tuple(s.D), tuple(s.H))
            )
            if score > new_score:
                score = new_score
                print(f"NEW SCORE: {score}")
        states = new_states

    return score


part_scores = []
for part in [1, 2]:
    part_scores.append(run(part))

for i, score in enumerate(part_scores):
    print(f"Part {i+1}: {score}")
