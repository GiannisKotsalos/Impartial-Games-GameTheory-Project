#!/usr/bin/env python3

import random
from functools import lru_cache
from typing import Optional

# 10 lines of four cells (rows, columns, diagonals)
LINES: list[tuple[int, int, int, int]] = [
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (8, 9, 10, 11),
    (12, 13, 14, 15),
    (0, 4, 8, 12),
    (1, 5, 9, 13),
    (2, 6, 10, 14),
    (3, 7, 11, 15),
    (0, 5, 10, 15),
    (3, 6, 9, 12),
]

SYMBOL: dict[int, str] = {1: "G", 2: "R", 0: "·"}
NAME: dict[int, str] = {1: "GREEN (G)", 2: "RED (R)"}


def display_board(board: list[int], last_move: Optional[int] = None) -> None:
    def cell(i: int) -> str:
        marker = "►" if i == last_move else " "
        if board[i] == 0:
            return f"{marker}{i + 1:02d}"
        return f"{marker} {SYMBOL[board[i]]}"

    sep = "─────────────────────"
    print()
    print(f"  ┌{sep}┐")
    for row in range(4):
        cells = [cell(row * 4 + col) for col in range(4)]
        print(f"  │ {cells[0]} │ {cells[1]} │ {cells[2]} │ {cells[3]} │")
        if row < 3:
            print(f"  ├{sep}┤")
    print(f"  └{sep}┘")
    print()


def current_player(board: tuple[int, ...]) -> int:
    return 1 if board.count(1) == board.count(2) else 2


def would_complete(board: tuple[int, ...], pos: int) -> bool:
    """True if the move at pos (before placement) completes a 4-cell line."""
    for line in LINES:
        if pos in line:
            if all(board[j] != 0 for j in line if j != pos):
                return True
    return False


def legal_moves(board: tuple[int, ...]) -> list[int]:
    return [i for i in range(16) if board[i] == 0]


def hot_cells(board: tuple[int, ...]) -> set[int]:
    """Empty cells where a move would immediately complete a line."""
    return {i for i in range(16) if board[i] == 0 and would_complete(board, i)}


@lru_cache(maxsize=None)
def is_win(board: tuple[int, ...]) -> bool:
    """
    WP (normal): there exists a legal move that wins immediately or leaves the opponent in an LP.
    Uses memoization (tuple as key).
    """
    player = current_player(board)
    moves = legal_moves(board)

    if not moves:
        return False

    for m in moves:
        if would_complete(board, m):
            return True
        nb = list(board)
        nb[m] = player
        if not is_win(tuple(nb)):
            return True

    return False


def find_best(board: tuple[int, ...]) -> int:
    """Optimal RED move: immediate win or a move to the opponent's LP; otherwise random."""
    player = current_player(board)
    moves = legal_moves(board)

    if is_win(board):
        for m in moves:
            if would_complete(board, m):
                return m
        for m in moves:
            if not would_complete(board, m):
                nb = list(board)
                nb[m] = player
                if not is_win(tuple(nb)):
                    return m

    return random.choice(moves)


def play(vs_computer: bool) -> None:
    board: tuple[int, ...] = (0,) * 16

    mode = "Human vs Computer" if vs_computer else "Human vs Human"

    print(f"\n{'═'*56}")
    print(f"  Impartial 4×4 Tic-Tac-Toe  ·  Normal variant")
    print(f"  {mode}")
    print(f"{'═'*56}")
    print("  Terminal rule: first completed line.")
    print("  ► The player who completed the line WINS.")
    if vs_computer:
        print("  GREEN = Human  |  RED = Computer")

    init_type = "WP" if is_win(board) else "LP"
    print(f"\n  Initial position: {init_type} for GREEN.")
    display_board(list(board))

    while True:
        player = current_player(board)
        moves = legal_moves(board)
        pos_lbl = "WP" if is_win(board) else "LP"
        hot = hot_cells(board)

        print(f"  {NAME[player]}  │  Position: {pos_lbl}  │  Hot cells: {sorted(h+1 for h in hot)}")

        if vs_computer and player == 2:
            move = find_best(board)
            print(f"  Computer chooses: cell {move + 1}.")
        else:
            available = sorted(m + 1 for m in moves)
            while True:
                raw = input(f"  Choose cell {available}: ").strip()
                try:
                    move = int(raw) - 1
                    if move in moves:
                        break
                    print("  ✗ Cell not available.")
                except ValueError:
                    print("  ✗ Enter an integer.")

        completes = would_complete(board, move)
        nb = list(board)
        nb[move] = player
        board = tuple(nb)
        display_board(list(board), last_move=move)

        if completes:
            winner = player
            loser = 3 - winner
            print(f"  ✔ Cell {move+1}: line completed by {NAME[player]}!")
            print()
            print(f"  🏆  WINNER : {NAME[winner]}")
            print(f"  💀  LOSS   : {NAME[loser]}")
            break


def choose(prompt: str, options: dict[str, str]) -> str:
    opts_str = "  /  ".join(f"({k}) {v}" for k, v in options.items())
    while True:
        ans = input(f"\n  {prompt}\n  {opts_str}\n  Choice: ").strip()
        if ans in options:
            return ans
        print("  ✗ Invalid choice.")


def main() -> None:
    print("\n╔════════════════════════════════════════════════════╗")
    print("║   Impartial 4×4 Tic-Tac-Toe     ║")
    print("╚════════════════════════════════════════════════════╝")

    while True:
        m = choose("Mode:", {"1": "Human vs Human",
                             "2": "Human vs Computer"})
        play(vs_computer=(m == "2"))

        again = choose("Play again?", {"y": "Yes", "n": "No"})
        if again == "n":
            print("\n  Goodbye!\n")
            break


if __name__ == "__main__":
    main()
