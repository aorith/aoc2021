#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    sys.exit(1)

file = sys.argv[1]

boards = []
board = []
with open(file, "r") as f:
    for idx, line in enumerate(f):
        if idx == 0:
            numbers = [int(x) for x in line.strip().split(",")]
            continue
        row = [int(x) for x in line.strip().split()]

        if not row:
            if board:
                boards.append(board)
                board = []
        else:
            board.append(row)

    if board:
        boards.append(board)


def is_winner(board):
    length = len(board[0])
    # rows
    for row in board:
        if sum([1 if n == "x" else 0 for n in row]) == length:
            return True
    # cols
    for idx in range(length):
        if sum([1 if r[idx] == "x" else 0 for r in board]) == length:
            return True

    return False


def calc_win(num, board):
    total = 0
    for row in board:
        for n in row:
            if isinstance(n, int):
                total += n
    print(total * num)
    return 0


winners_idx = []
winners_num = []
winners_board = []
for num in numbers:
    for idx, board in enumerate(boards):
        for idx_r, row in enumerate(board):
            if num not in row:
                continue
            board[idx_r] = ["x" if n == num else n for n in row]
        boards[idx] = board
        if idx not in winners_idx and is_winner(board):
            winners_idx.append(idx)
            winners_board.append(board.copy())
            winners_num.append(num)

last_winner_num = winners_num[-1]
last_winner_board = winners_board[-1]
calc_win(last_winner_num, last_winner_board)
