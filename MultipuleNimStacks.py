import random


def choose_parameters():
    n1 = random.randint(8, 11)
    n2 = random.randint(8, 11)
    n3 = random.randint(8, 11)
    max_removed = random.choice([2, 3, 4, 5])
    return [n1, n2, n3], max_removed


def grundy(n, max_removed):
    """Grundy value of a pile of size n with max removal k: g(n) = n mod (k+1)."""
    return n % (max_removed + 1)


def nim_sum(piles, max_removed):
    """XOR of the Grundy values of all piles."""
    s = 0
    for p in piles:
        s ^= grundy(p, max_removed)
    return s


def computer_move(piles, max_removed):
    """
    LP (S=0): uniform random legal move.
    WP (S≠0): optimal move via Grundy / XOR.
    """
    k = max_removed
    g = [grundy(p, k) for p in piles]
    S = g[0] ^ g[1] ^ g[2]

    if S == 0:
        all_moves = []
        for i in range(3):
            for r in range(1, min(k, piles[i]) + 1):
                all_moves.append((i, r))
        pile_idx, remove = random.choice(all_moves)
        print(
            f"  [Computer — LP] Random move: removes {remove} from P{pile_idx + 1}"
        )
        return pile_idx, remove

    msb_S = S.bit_length() - 1
    chosen = -1
    for i in range(3):
        if (g[i] >> msb_S) & 1:
            chosen = i
            break

    si = g[chosen]
    si_new = si ^ S
    remove = si - si_new

    print(
        f"  [Computer — WP] Grundy={g}, S={S}, "
        f"P{chosen + 1}: {si}→{si_new}, removes {remove}"
    )
    return chosen, remove


def print_state(piles, current_player, max_removed):
    g = [grundy(p, max_removed) for p in piles]
    S = g[0] ^ g[1] ^ g[2]
    pos_note = "loss (LP)" if S == 0 else "win (WP)"
    col_w = 8
    label_w = 14
    print("\n" + "=" * 56)
    print(f"  {'':{label_w}}{'P1':>{col_w}}{'P2':>{col_w}}{'P3':>{col_w}}")
    print(f"  {'Sticks':<{label_w}}{piles[0]:>{col_w}}{piles[1]:>{col_w}}{piles[2]:>{col_w}}")
    print(
        f"  {'Grundy':<{label_w}}{g[0]:>{col_w}}{g[1]:>{col_w}}{g[2]:>{col_w}}    XOR = {S}"
    )
    print(f"  Max removal per move: {max_removed}")
    print(f"  Turn: {current_player}  — {pos_note} for the player to move")
    print("=" * 56)


def get_human_move(piles, max_removed):
    while True:
        try:
            pile_idx = int(input("  Choose pile (1, 2, or 3): ")) - 1
            if pile_idx not in (0, 1, 2):
                print("  Please choose 1, 2, or 3.")
                continue
            if piles[pile_idx] == 0:
                print("  That pile is empty! Choose another.")
                continue
            limit = min(max_removed, piles[pile_idx])
            remove = int(
                input(f"  How many sticks from P{pile_idx + 1} (1-{limit})? ")
            )
            if 1 <= remove <= limit:
                return pile_idx, remove
            print(f"  Invalid move. Choose from 1 to {limit}.")
        except ValueError:
            print("  Please enter an integer.")


def play_two_players():
    print("\n╔═══════════════════════════════════════════╗")
    print("║   3 NIM PILES — TWO PLAYERS               ║")
    print("╚═══════════════════════════════════════════╝")

    piles, max_removed = choose_parameters()

    print("\n--- Match parameters ---")
    print(f"  Piles           : {piles[0]} | {piles[1]} | {piles[2]}")
    print(f"  Max removal     : {max_removed}")

    players = ["GREEN", "RED"]
    current = 0

    while sum(piles) > 0:
        print_state(piles, players[current], max_removed)
        pile_idx, remove = get_human_move(piles, max_removed)
        piles[pile_idx] -= remove
        print(
            f"  → {players[current]} removed {remove} from P{pile_idx + 1}. "
            f"Piles: {piles}"
        )

        if sum(piles) == 0:
            print("\n" + "=" * 50)
            print(f"  WINNER: {players[current]}!")
            print("=" * 50)
            return

        current = 1 - current


def play_vs_computer():
    print("\n╔══════════════════════════════════════════════╗")
    print("║   3 NIM PILES — HUMAN vs COMPUTER            ║")
    print("╚══════════════════════════════════════════════╝")
    print("  GREEN = You (first)")
    print("  RED   = Computer")

    piles, max_removed = choose_parameters()

    print("\n--- Match parameters ---")
    print(f"  Piles           : {piles[0]} | {piles[1]} | {piles[2]}")
    print(f"  Max removal     : {max_removed}")

    players = ["GREEN", "RED"]
    current = 0

    while sum(piles) > 0:
        print_state(piles, players[current], max_removed)

        if current == 0:
            pile_idx, remove = get_human_move(piles, max_removed)
        else:
            pile_idx, remove = computer_move(piles, max_removed)

        piles[pile_idx] -= remove
        print(
            f"  → {players[current]} removed {remove} from P{pile_idx + 1}. "
            f"Piles: {piles}"
        )

        if sum(piles) == 0:
            print("\n" + "=" * 50)
            print(f"  WINNER: {players[current]}!")
            print("=" * 50)
            return

        current = 1 - current


def choose_mode() -> str:
    print("\n╔══════════════════════════════════════╗")
    print("║        3 NIM PILES                   ║")
    print("╚══════════════════════════════════════╝")
    print("  1. Two players (human vs human)")
    print("  2. Human vs computer")
    print("  q. Exit")
    while True:
        c = input("\nChoose mode (1 / 2 / q): ").strip().lower()
        if c in ("1", "2", "q", "quit"):
            return c
        print("Please enter 1, 2, or q.")


def main() -> None:
    print("\nWelcome. Choose a mode and play a match.")
    while True:
        mode = choose_mode()
        if mode in ("q", "quit"):
            print("Goodbye!")
            break

        play_fn = play_two_players if mode == "1" else play_vs_computer

        while True:
            play_fn()
            again = input(
                "\nPlay another match with the same mode? (y/n): "
            ).strip().lower()
            if again not in ("y", "yes"):
                break


if __name__ == "__main__":
    main()
