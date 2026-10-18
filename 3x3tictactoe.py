#!/usr/bin/env python3

import random
from functools import lru_cache
from typing import Optional

LINES: list[tuple[int, int, int]] = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]

# Reflection through the center (cell 4) — used in misère (copycat)
MIRROR: dict[int, int] = {0: 8, 8: 0, 2: 6, 6: 2, 1: 7, 7: 1, 3: 5, 5: 3}
CENTER = 4

SYMBOL: dict[int, str] = {1: "G", 2: "R", 0: "·"}
NAME: dict[int, str] = {1: "GREEN (G)", 2: "RED (R)"}


def display_board(board: list[int], last_move: Optional[int] = None) -> None:
    def cell(i: int) -> str:
        marker = "►" if i == last_move else " "
        if board[i] == 0:
            return f"{marker}{i + 1:02d}"
        return f"{marker} {SYMBOL[board[i]]}"

    sep = "───────────────"
    print()
    print(f"  ┌{sep}┐")
    for row in range(3):
        cells = [cell(row * 3 + col) for col in range(3)]
        print(f"  │ {cells[0]} │ {cells[1]} │ {cells[2]} │")
        if row < 2:
            print(f"  ├{sep}┤")
    print(f"  └{sep}┘")
    print()


def current_player(board: tuple[int, ...]) -> int:
    return 1 if board.count(1) == board.count(2) else 2


def would_complete(board: tuple[int, ...], pos: int) -> bool:
    """True if the move at pos completes a triple (row/column/diagonal)."""
    for line in LINES:
        if pos in line:
            if all(board[j] != 0 for j in line if j != pos):
                return True
    return False


def legal_moves(board: tuple[int, ...]) -> list[int]:
    return [i for i in range(9) if board[i] == 0]


def hot_cells(board: tuple[int, ...]) -> set[int]:
    """Empty cells where a move would immediately complete a line."""
    return {i for i in range(9) if board[i] == 0 and would_complete(board, i)}


@lru_cache(maxsize=None)
def is_win(board: tuple[int, ...], misere: bool) -> bool:
    """
    WP: there exists a legal move that wins (normal) or leaves the opponent in an LP.
    In misère, completing a line does not count as an immediate win here.
    """
    player = current_player(board)
    moves = legal_moves(board)

    if not moves:
        return False

    for m in moves:
        if would_complete(board, m):
            if not misere:
                return True
        else:
            nb = list(board)
            nb[m] = player
            if not is_win(tuple(nb), misere):
                return True

    return False


def copycat_move(board: tuple[int, ...]) -> Optional[int]:
    """
    Misère, GREEN does not occupy center: RED answers on the mirrored cell
    so the nim-sum stays 0 until GREEN is forced to complete a line.
    """
    for i in range(9):
        if i == CENTER:
            continue
        if board[i] == 1:
            m = MIRROR[i]
            if board[m] == 0:
                return m
    return None


def non_hot_best(board: tuple[int, ...], misere: bool) -> Optional[int]:
    """Misère with GREEN on center: prefer a non-hot cell that leaves RED in an LP."""
    moves = legal_moves(board)
    non_hot = [m for m in moves if not would_complete(board, m)]

    if not non_hot:
        return None

    for m in non_hot:
        nb = list(board)
        nb[m] = 1
        if not is_win(tuple(nb), misere):
            return m

    return random.choice(non_hot)


def find_best(board: tuple[int, ...], misere: bool) -> int:
    """
    Optimal RED move.
    Normal: immediate win or a move to the opponent's LP.
    Misère: copycat if GREEN does not occupy center, otherwise non-hot / backward-style moves.
    """
    player = current_player(board)
    moves = legal_moves(board)

    if not misere:
        if is_win(board, misere):
            for m in moves:
                if would_complete(board, m):
                    return m
            for m in moves:
                nb = list(board)
                nb[m] = player
                if not is_win(tuple(nb), misere):
                    return m
        return random.choice(moves)

    green_has_center = board[CENTER] == 1

    if not green_has_center:
        cm = copycat_move(board)
        if cm is not None and cm in moves:
            return cm
        if is_win(board, misere):
            for m in moves:
                if not would_complete(board, m):
                    nb = list(board)
                    nb[m] = player
                    if not is_win(tuple(nb), misere):
                        return m
        return random.choice(moves)

    if is_win(board, misere):
        for m in moves:
            if not would_complete(board, m):
                nb = list(board)
                nb[m] = player
                if not is_win(tuple(nb), misere):
                    return m
    return random.choice(moves)


def play(misere: bool, vs_computer: bool) -> None:
    board: tuple[int, ...] = (0,) * 9

    variant = "Misère" if misere else "Normal"
    mode = "Human vs Computer" if vs_computer else "Human vs Human"

    print(f"\n{'═'*52}")
    print(f"  Impartial 3×3 Tic-Tac-Toe  ·  {variant} Variant")
    print(f"  {mode}")
    print(f"{'═'*52}")
    print("  Terminal rule: first completed line.")
    if misere:
        print("  ► The player who completed the line LOSES.")
    else:
        print("  ► The player who completed the line WINS.")
    if vs_computer:
        print("  GREEN = Human  |  RED = Computer")

    init_type = "WP" if is_win(board, misere) else "LP"
    print(f"\n  Initial position: {init_type} for GREEN.")
    display_board(list(board))

    while True:
        player = current_player(board)
        moves = legal_moves(board)
        pos_lbl = "WP" if is_win(board, misere) else "LP"
        hot = hot_cells(board)

        if misere and vs_computer and player == 2:
            if board[CENTER] == 1:
                print("  [RED strategy: recursive optimization — GREEN occupies the center]")
            else:
                print("  [RED strategy: symmetric reply through the center — Nim-sum = 0]")

        print(f"  {NAME[player]}  │  Position: {pos_lbl}  │  Hot cells: {sorted(h+1 for h in hot)}")

        if vs_computer and player == 2:
            move = find_best(board, misere)
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
            winner = (3 - player) if misere else player
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
    print("\n╔══════════════════════════════════════════════════╗")
    print("║  CEID_NE0509  ·  P3: Impartial 3×3 Tic-Tac-Toe   ║")
    print("╚══════════════════════════════════════════════════╝")

    while True:
        v = choose("Variant:", {"1": "Normal", "2": "Misère"})
        m = choose("Mode:", {"1": "Human vs Human",
                             "2": "Human vs Computer"})
        play(misere=(v == "2"), vs_computer=(m == "2"))

        again = choose("Play again?", {"y": "Yes", "n": "No"})
        if again == "n":
            print("\n  Goodbye!\n")
            break


if __name__ == "__main__":
    main()
