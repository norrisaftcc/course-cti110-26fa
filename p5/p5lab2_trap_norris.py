# CTI 110
# P5LAB2 - The Trap
# norris
# 10/22/26

# THE TRAP -- read this before you run the file.
#
# In M3BONUS, each door was a function. That was good.
# This file goes one step further, and that step is a trap:
# a room function CALLS the next room function.
#
#   jetty() calls tower() to walk up the hill.
#   tower() calls jetty() to walk back down.
#
# Each call starts INSIDE the one before it. The old call never ends.
# It just waits. Walk back and forth, and the waiting calls pile up.
# Each room prints how deep the pile is: (calls deep: N).
#
# Python keeps the pile to about 1,000 calls. Then it stops the program:
#   RecursionError: maximum recursion depth exceeded
# Type auto at the start to watch that happen. Read the traceback together.
#
# Look for the LATE LINE in jetty(). It sits after a room call, so it runs
# only when that call ends. Walk a few times, then stop. The late lines
# print last, in reverse order, as the pile unwinds.
#
# p5lab2_norris.py fixes the trap: a room RETURNS the next room's id.


# ask() shows a prompt and returns the answer, trimmed and in lower case
def ask(prompt):
    return input(prompt).strip().lower()


# A yes/no question. The while loop repeats until we get y or n.
def ask_yes_no(prompt):
    answer = ask(prompt)
    while answer != "y" and answer != "n":
        print("Please type y or n.")
        answer = ask(prompt)
    return answer


# depth = how many room calls are waiting. auto = True walks on its own.
def jetty(depth, auto):
    print()
    print(f"S1. THE BROKEN JETTY  (calls deep: {depth})")
    print("Half the jetty lies in the lake.")
    if auto:
        tower(depth + 1, auto)         # THE TRAP: a room calls a room
    elif ask_yes_no("Walk up to the tower? (y/n): ") == "y":
        tower(depth + 1, auto)         # THE TRAP: a room calls a room
        print(f"  (late line: jetty at depth {depth} ends now)")   # THE LATE LINE


def tower(depth, auto):
    print()
    print(f"S2. THE TOWER SHELL  (calls deep: {depth})")
    print("Rubble, a stair up the wall, and crows.")
    if auto:
        jetty(depth + 1, auto)         # THE TRAP again, the other way
    elif ask_yes_no("Walk back down to the jetty? (y/n): ") == "y":
        jetty(depth + 1, auto)         # THE TRAP again, the other way


def main():
    # INPUT -- walk yourself, or let the rooms walk on their own
    mode = ask("Type walk to walk yourself, or auto to let the rooms walk: ")
    while mode != "walk" and mode != "auto":
        print("Please type walk or auto.")
        mode = ask("Type walk to walk yourself, or auto to let the rooms walk: ")

    # PROCESSING -- the first room call. Every other call happens inside it.
    jetty(1, mode == "auto")

    # OUTPUT -- this line runs only after EVERY room call has ended
    print()
    print("The walk is over.")


# at the bottom -- start the program
main()
