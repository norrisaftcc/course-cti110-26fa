# CTI 110
# P5LAB2 - Functions
# norris
# 10/22/26

# THE FIX for p5lab2_trap_norris.py.
# A room never calls a room. A room RETURNS the id of the next room,
# as a string, or "end". One while loop in main() moves the hero.
# Each room finishes before the next one starts, so calls never pile up.

# WHAT THIS TEACHES
#   - Parameters: values a caller hands IN to a function (hero_name).
#   - return: a value a function hands BACK to its caller (the next room id).
#   - A "game loop": one while loop decides what runs next. The rooms only
#     report where to go. They do not go there themselves.
#   - Returning TWO values with a tuple, and catching them: a, b = f()
#   - Why this beats the trap: when a room returns, it is OVER. Nothing
#     waits on the pile. The pile does not grow.
# Think of main() as a bus driver and each room as a stop. The stops
# say "next stop: tower". They do not drive the bus.


# ask() shows a prompt and returns the answer, trimmed and in lower case
# .strip() removes spaces around the answer. .lower() makes "Y" into "y".
def ask(prompt):
    return input(prompt).strip().lower()


# Ask until the answer is one of the choices in the list
# "not in" checks the list. The loop keeps asking until the answer is on it.
def ask_choice(prompt, choices):
    answer = ask(prompt)
    while answer not in choices:
        print("That is not one of the choices. Try again.")
        answer = ask(prompt)
    return answer


# hero_name is a PARAMETER. The caller fills it in.
# return hands the next room's id back to the caller.
def docks(hero_name):
    print()
    print("The Fort docks. Captain Maren coils a wet rope and does not smile.")
    print(f"\"Row to the Isle of Old Stone, {hero_name}.\"")
    # Call ask_choice, compare its answer with "y" right away.
    if ask_choice("Row to the island? (y/n): ", ["y", "n"]) == "y":
        return "jetty"
    # A return ends the function at once. Reaching this line means "n".
    return "end"


def jetty(hero_name):
    print()
    print("S1. THE BROKEN JETTY")
    print("Half the jetty lies in the lake. A rope burn on a post is fresh:")
    print("someone else lands here.")
    print(f"{hero_name} stands on the jetty.")
    print("  1. Walk up to the tower")
    print("  2. Row home")
    pick = ask_choice("Pick 1 or 2: ", ["1", "2"])
    if pick == "1":
        return "tower"
    return "end"


def tower(hero_name):
    print()
    print("S2. THE TOWER SHELL")
    print("A round shell of stone, thirty feet across, open to the sky.")
    print("Rubble covers the floor. A stair climbs the wall to a broken top.")
    print(f"{hero_name} looks around.")
    print("  1. Walk down to the jetty")
    print("  2. Look in the cottage")
    print("  3. Search the rubble")
    pick = ask_choice("Pick 1, 2 or 3: ", ["1", "2", "3"])
    if pick == "1":
        return "jetty"
    elif pick == "2":
        return "cottage"
    else:
        # The only way left is "3". This room ends the game, so it says so.
        print("Under the rubble lies a trapdoor of black oak.")
        print("The cellar waits for another day.")
        return "end"


def cottage(hero_name):
    print()
    print("S3. THE KEEPER'S COTTAGE")
    print("No roof. Ash in the hearth, less than a week old. A tin of lamp")
    print("oil. On the door, a chalked eye with a line through it.")
    print(f"{hero_name} walks back to the tower.")
    # No choice here: the cottage always sends the hero back to the tower.
    return "tower"


# One turn passes. Python cannot change main's numbers from in here,
# so we RETURN both new values. main() catches them: turn, torch = tick(...)
# (turn and torch here are COPIES. Changing them does not touch main's.)
def tick(turn, torch):
    turn = turn + 1
    torch = torch - 1
    print(f"Turn {turn}. Torch: {torch} of 6.")
    return turn, torch


def main():
    # INPUT
    hero_name = input("What is your hero's name? ").strip()
    turn = 0
    torch = 6
    print(f"You light a torch. It will burn {torch} turns.")

    # PROCESSING -- the game loop. room holds the id of the room we are in.
    room = "docks"
    while room != "end":
        # Call the room, and SAVE what it returns. That is the next room.
        # Each pass: run ONE room, finish it, then come back to this loop.
        # (An id that matches no branch would leave room unchanged and loop
        # forever. P7LAB1 replaces this chain with a dictionary.)
        if room == "docks":
            room = docks(hero_name)
        elif room == "jetty":
            room = jetty(hero_name)
        elif room == "tower":
            room = tower(hero_name)
        elif room == "cottage":
            room = cottage(hero_name)

        # The clock ticks once per room
        # Two names on the left catch the two values the function returns.
        turn, torch = tick(turn, torch)
        # The torch is a countdown that can end the game from outside the room.
        # "and room != 'end'" skips the torch message if the hero already left.
        if torch <= 0 and room != "end":
            print("Your torch gutters out. In the dark you feel your way back to")
            print("the boat. The delve is over for today.")
            room = "end"

    # OUTPUT
    print()
    print(f"The delve ends on turn {turn}.")


# at the bottom -- start the program
main()
