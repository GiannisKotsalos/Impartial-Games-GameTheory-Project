import random


def choose_parameters():
    num_sticks = random.randint(16, 25)
    max_removed = random.choice([2, 3, 4, 5])
    return num_sticks, max_removed


def choose_variant():
    print("\nChoose game variant:")
    print("  1. Normal (who takes the last stick wins)")
    print("  2. Misère (who takes the last stick loses)")
    while True:
        choice = input("Choice (1 or 2): ").strip()
        if choice in ("1", "2"):
            return choice == "1"
        print("Please enter 1 or 2.")


def print_state(sticks, current_player, max_removed):
    print("\n" + "=" * 40)
    print(f"  Sticks remaining: {sticks}")
    print(f"  Max removal per move: {max_removed}")
    print(f"  Turn: {current_player}")
    print("=" * 40)


def get_move(sticks, max_removed, player):
    while True:
        try:
            move = int(
                input(
                    f"{player}, how many sticks do you want to remove (1-{min(max_removed, sticks)})? "
                )
            )
            if 1 <= move <= min(max_removed, sticks):
                return move
            print(f"  Invalid move. Choose from 1 to {min(max_removed, sticks)}.")
        except ValueError:
            print("  Please enter an integer.")


def is_losing_position(sticks, max_removed, normal_play):
    """
    Returns True if the position is losing for the player to move.
    Normal: loss if n mod (k+1) == 0
    Misère: loss if n mod (k+1) == 1
    """
    k = max_removed
    if normal_play:
        return sticks % (k + 1) == 0
    return sticks % (k + 1) == 1


def computer_move(sticks, max_removed, normal_play):
    """
    Winning position → optimal move (leaves opponent in a losing position)
    Losing position → random legal move
    """
    k = max_removed

    if is_losing_position(sticks, k, normal_play):
        move = random.randint(1, min(k, sticks))
        print(f"  [Computer — LP] Random choice: {move} stick(s)")
        return move

    if normal_play:
        move = sticks % (k + 1)
    else:
        move = (sticks - 1) % (k + 1)
        if move == 0:
            move = k
    print(f"  [Computer — WP] Optimal move: {move} stick(s)")
    return move


def human_move(sticks, max_removed):
    while True:
        try:
            move = int(
                input(
                    f"GREEN, how many sticks do you remove (1-{min(max_removed, sticks)})? "
                )
            )
            if 1 <= move <= min(max_removed, sticks):
                return move
            print(f"  Invalid move. Choose from 1 to {min(max_removed, sticks)}.")
        except ValueError:
            print("  Please enter an integer.")


def play_two_players():
    print("\n╔══════════════════════════════════════╗")
    print("║     NIM STACK — TWO PLAYERS          ║")
    print("╚══════════════════════════════════════╝")

    num_sticks, max_removed = choose_parameters()
    normal_play = choose_variant()

    variant_name = "NORMAL" if normal_play else "MISÈRE"
    print("\n--- Match parameters ---")
    print(f"  Number of sticks: {num_sticks}")
    print(f"  Max removal     : {max_removed}")
    print(f"  Variant         : {variant_name}")

    players = ["GREEN", "RED"]
    current = 0
    sticks = num_sticks

    while sticks > 0:
        print_state(sticks, players[current], max_removed)
        move = get_move(sticks, max_removed, players[current])
        sticks -= move
        print(f"  → {players[current]} removed {move} stick(s). Remaining: {sticks}")

        if sticks == 0:
            print("\n" + "=" * 40)
            if normal_play:
                print(f"  WINNER: {players[current]}!")
            else:
                winner = players[1 - current]
                print(f"  WINNER: {winner}!")
                print(f"  ({players[current]} took the last stick and lost)")
            print("=" * 40)
            return

        current = 1 - current


def play_vs_computer():
    print("\n╔══════════════════════════════════════╗")
    print("║  NIM STACK — HUMAN vs COMPUTER       ║")
    print("╚══════════════════════════════════════╝")
    print("  GREEN = You (first)")
    print("  RED   = Computer")

    num_sticks, max_removed = choose_parameters()
    normal_play = choose_variant()

    variant_name = "NORMAL" if normal_play else "MISÈRE"
    print("\n--- Match parameters ---")
    print(f"  Number of sticks: {num_sticks}")
    print(f"  Max removal     : {max_removed}")
    print(f"  Variant         : {variant_name}")

    sticks = num_sticks
    current = 0

    while sticks > 0:
        player_name = "GREEN" if current == 0 else "RED"
        print_state(sticks, player_name, max_removed)

        if is_losing_position(sticks, max_removed, normal_play):
            print(f"  [Info] Losing position (LP) for {player_name}.")
        else:
            print(f"  [Info] Winning position (WP) for {player_name}.")

        if current == 0:
            move = human_move(sticks, max_removed)
        else:
            move = computer_move(sticks, max_removed, normal_play)

        sticks -= move
        print(f"  → {player_name} removed {move} stick(s). Remaining: {sticks}")

        if sticks == 0:
            print("\n" + "=" * 40)
            if normal_play:
                winner = player_name
            else:
                winner = "GREEN" if current == 1 else "RED"
            print(f"  WINNER: {winner}!")
            if not normal_play:
                print(f"  ({player_name} took the last stick and lost)")
            print("=" * 40)
            return

        current = 1 - current


def choose_mode() -> str:
    print("\n╔══════════════════════════════════════╗")
    print("║         NIM STACK                    ║")
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
