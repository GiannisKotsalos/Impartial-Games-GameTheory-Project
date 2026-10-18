#  Impartial Games: Nim & Tic-Tac-Toe

Four terminal games with perfect-play computer opponents (computer solvers) , built as **Assignment** for *Algorithmic Game Theory* (Computer Engineering & Informatics Dept., University of Patras, 2025-2026).

All games are **impartial**: both players have exactly the same moves available, so all that matters is whose turn it is. The "AI" (computer solver) relies on combinatorial game theory (Sprague-Grundy theory, Nim-sums, symmetry/copycat strategies, and backward induction with memoization) to play optimally whenever it is in a winning position.

---

## Contents

| File | Game | Variants |
|---|---|---|
| [`NimStack.py`](NimStack.py) | Nim, single stack, capped removal | Normal & Misere |
| [`MultipuleNimStacks.py`](MultipuleNimStacks.py) | Nim, three stacks, capped removal | Normal |
| [`3x3tictactoe.py`](3x3tictactoe.py) | Impartial 3x3 Tic-Tac-Toe | Normal & Misere |
| [`4x4tictactoe.py`](4x4tictactoe.py) | Impartial 4x4 Tic-Tac-Toe | Normal |

Every game supports **Human vs Human** and **Human vs Computer**. Against the computer, you are **GREEN** (first to move) and the computer is **RED**.

---

## 🚀 Quick start

**Requirements:** Python 3.9 or newer. No external libraries, standard library only.

```bash

python3 NimStack.py
python3 MultipuleNimStacks.py
python3 3x3tictactoe.py
python3 4x4tictactoe.py
```

Menus are number-driven: type the option number and press Enter. Answer `y` / `n` when asked for a new game, and use `q` to quit the Nim menus.

---

##  Terminal board schema

Both Tic-Tac-Toe games draw the board directly in the terminal. Empty cells show their **cell number** (the number you type to play there), taken cells show the owner's letter (**G** for Green, **R** for Red), and the last move is flagged with `►`.

### 3x3 board

Cell numbering:

```
  ┌──────┬──────┬──────┐
  │  01  │  02  │  03  │
  ├──────┼──────┼──────┤
  │  04  │  05  │  06  │
  ├──────┼──────┼──────┤
  │  07  │  08  │  09  │
  └──────┴──────┴──────┘
```

Example mid-game position (Misere, Green holds the centre and just played cell 3):

```
  RED (R)  |  Position: P  |  Hot cells: [2, 7, 9]

  ┌──────┬──────┬──────┐
  │  R   │  02  │ ► G  │
  ├──────┼──────┼──────┤
  │  04  │  G   │  06  │
  ├──────┼──────┼──────┤
  │  07  │  08  │  09  │
  └──────┴──────┴──────┘

  Choose a cell [2, 4, 6, 7, 8, 9]:
```

*Hot cells* are empty cells that would complete a line immediately, which ends the game (a win in normal play, a loss in misere play).

### 4x4 board

Cell numbering:

```
  ┌──────┬──────┬──────┬──────┐
  │  01  │  02  │  03  │  04  │
  ├──────┼──────┼──────┼──────┤
  │  05  │  06  │  07  │  08  │
  ├──────┼──────┼──────┼──────┤
  │  09  │  10  │  11  │  12  │
  ├──────┼──────┼──────┼──────┤
  │  13  │  14  │  15  │  16  │
  └──────┴──────┴──────┴──────┘
```

Example mid-game position (Red just played cell 3):

```
  GREEN (G)  |  Hot cells: [15]

  ┌──────┬──────┬──────┬──────┐
  │  01  │  02  │ ► R  │  04  │
  ├──────┼──────┼──────┼──────┤
  │  05  │  G   │  G   │  08  │
  ├──────┼──────┼──────┼──────┤
  │  09  │  10  │  R   │  12  │
  ├──────┼──────┼──────┼──────┤
  │  13  │  14  │  15  │  16  │
  └──────┴──────┴──────┴──────┘

  Choose a cell [1, 2, 4, 5, 8, 9, 10, 12, 13, 14, 15, 16]:
```

### Symmetry pairs

The mirror structure that the 3x3 copycat strategy relies on (the centre `M` has no mirror):

```
  3x3 mirror pairs            4x4 point-symmetric pairs
  (around the centre)         (around the board centre)

  C1  E1  C2                  1-16   2-15   3-14   4-13
  E2  M   E3                  5-12   6-11   7-10   8-9
  C3  E4  C4

  1-9, 2-8, 3-7, 4-6
```

---

##  Games and theory

### Terminology

- **N-position:** the player to move wins with optimal play.
- **P-position:** the player to move loses against optimal play.
- **Normal play:** the player who makes the last / terminating move **wins**.
- **Misere play:** the player who makes the last / terminating move **loses**.

From N-positions the AI plays the optimal move. From P-positions it plays a uniformly random legal move, since nothing can save it against perfect play.

### 1. Nim, single stack (`NimStack.py`)

A stack of **16-25** sticks (random). Each turn a player removes **1 to k** sticks, where **k in {2, 3, 4, 5}** is chosen randomly and stays fixed for the game.

| Variant | Losing position (P) | Optimal move from an N-position |
|---|---|---|
| Normal | `n mod (k+1) = 0` | remove `n mod (k+1)` |
| Misere | `n mod (k+1) = 1` | remove `(n - 1) mod (k+1)` |

From a P-position, whatever `x` the player removes, the opponent answers with `k+1-x` and keeps the pile on the same residue. In misere play the target residue is 1, so the player facing a single stick is forced to take it and lose.

### 2. Three Nim stacks (`MultipuleNimStacks.py`)

Three stacks of **8-11** sticks each (random), with a shared cap **k in {2, 3, 4, 5}**. Normal play only.

Each stack behaves like a Nim heap with Grundy value:

```
g(n) = n mod (k+1)
```

The position's Nim-sum is `S = g(n1) XOR g(n2) XOR g(n3)`:

- `S = 0` : P-position
- `S != 0` : N-position

**Winning algorithm (N-position):**

1. Compute `g_i` for each stack and the Nim-sum `S`.
2. Pick a stack whose Grundy value has a 1 in the same position as the most significant bit of `S`.
3. Reduce that stack's Grundy value from `g_i` to `g_i XOR S`, i.e. remove `g_i - (g_i XOR S)` sticks. This is always within `1..k`.

Working on reduced Grundy values rather than raw stack sizes guarantees the move respects the removal limit.

### 3. Impartial 3x3 Tic-Tac-Toe (`3x3tictactoe.py`)

Each player writes with their own marker, but the game ends the first time **any row, column or diagonal is completely filled**, regardless of who owns the markers.

- **Normal:** the player who completes the line **wins**.
- **Misere:** the player who completes the line **loses**.

**Normal play:** the first player is in an N-position. Green takes the centre, then answers every Red move with its **mirror cell**. Red's first move `y` and Green's reply `mirror(y)` already complete the line `y - M - mirror(y)`, so Green wins on his second move.

**Misere play:**

- If Green does **not** take the centre, Green is in a P-position. Red answers every Green move with its mirror cell. This keeps the board symmetric, so Red can never complete a line before Green does, and the centre becomes a hot cell that nobody can play. Green is eventually forced to complete a line.
- If Green **takes the centre**, copycat is unavailable. Green wins by always choosing **non-hot cells** (cells that do not complete a line), which eventually forces Red to close one.

Implementation highlights:

- `is_win()` classifies positions by backward induction with `lru_cache`.
- `hot_cells()` and `would_complete()` detect cells that would close a line.
- `copycat_move()` implements the mirror strategy, and `find_best()` chooses between copycat and search-based play.

### 4. Impartial 4x4 Tic-Tac-Toe (`4x4tictactoe.py`)

Same idea on a 4x4 board, **normal play only**. The game ends when any of the **10 lines** (4 rows, 4 columns, 2 diagonals) is filled.

- Exhaustive search shows the initial position is a **P-position**: with perfect play the **second player (Red) wins**.
- Red's strategy: answer a Green move at cell `x` with the point-symmetric cell `17 - x`, unless a line can be completed immediately, in which case complete it. Green can never complete a line first.
- The strategy-stealing argument does not apply here: an extra filled cell is not harmless, since it brings lines closer to completion.
- Practical consequence: in Human vs Computer mode, a perfect Red cannot be beaten by Green.
- The AI finds optimal moves with **memoized backward induction** (`is_win`): take an immediate line-completing move, or move to a position where the opponent is in a P-position.

---

## Implementation notes

- **Language:** Python 3, text-based terminal interface.
- **Randomness:** `random` is used for initial parameters (stack sizes, `k`) and for moves from losing positions.
- **Memoization:** board states are immutable `tuple`s so they can be cached with `functools.lru_cache`, avoiding recomputation in the game-tree search.
- **Performance:** the 4x4 solver searches a much larger game tree than the 3x3 one, so the first evaluation may take noticeably longer and use more memory.

---

##  Repository structure

```
.
├── NimStack.py              # Single-stack Nim (normal & misere)
├── MultipuleNimStacks.py    # Three-stack Nim (Grundy / Nim-sum)
├── 3x3tictactoe.py          # Impartial 3x3 Tic-Tac-Toe (normal & misere)
├── 4x4tictactoe.py          # Impartial 4x4 Tic-Tac-Toe (normal)
└── README.md
```

---

## Concepts demonstrated

- Sprague-Grundy theorem and Grundy values
- Nim-sum (XOR) strategy
- Normal vs. misere play
- N-/P-position classification
- Mirror (copycat) strategies
- Point-reflection symmetry strategies
- Backward induction with memoization

---

##  Author

**Ioannis Kotsalos**
Computer Engineering & Informatics, University of Patras
Course: *Algorithmic Game Theory*, academic year 2025-2026

---

## License

 This project was created for educational purposes.
