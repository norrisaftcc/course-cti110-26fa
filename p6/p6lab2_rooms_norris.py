# CTI 110
# P6LAB2 - Rooms as Data
# norris
# 11/5/26

# Three rooms, stored as DATA, not as functions.
# ROOMS is a dictionary. Each value is another dictionary (a dict of dicts).
# "exits" maps the id of the next room to the words the player sees.
# Read it, predict it, run it. Today we do not change it.

# WHAT THIS TEACHES
#   - Data-driven design: the rooms are plain data. ONE loop plays them all.
#     To add a fourth room, add a few lines of data. Add no new code.
#   - A dict inside a dict: ROOMS["tower"]["title"] looks up the room, then
#     looks up the title inside it.
#   - Looping over a dict gives its KEYS. Then you use each key to look up
#     its value.
#   - Two lists kept in step: the number a player types, and the room that
#     number means. Person counts from 1, list counts from 0.
#   - Validation with a while loop (same shape as P4LAB2).
# Compare with p5lab2_norris.py, where every room was its own function.
# Same kind of game, much less plumbing. The rooms did not complain.

# The outer key is the room's id. Each room is a dict with three fields:
#   "title" and "text" are strings to print.
#   "exits" is a dict again: {next room id : words the player sees}.
ROOMS = {
    "jetty": {
        "title": "S1. The Broken Jetty",
        "text": "Half the jetty lies in the lake. A rope burn on a post is fresh.",
        "exits": {"tower": "Walk up to the tower"},
    },
    "tower": {
        "title": "S2. The Tower Shell",
        "text": "Rubble covers the floor. Crows watch you from the rim.",
        "exits": {"jetty": "Walk down to the jetty", "cottage": "Look in the cottage"},
    },
    "cottage": {
        "title": "S3. The Keeper's Cottage",
        "text": "No roof. Ash in the hearth, less than a week old.",
        "exits": {"tower": "Walk back to the tower"},
    },
}


def main():
    room = "jetty"          # the id of the room we stand in
    answer = ""             # must exist before the loop test reads it
    while answer != "q":
        # OUTPUT -- look up this room's dict, then show its title and text
        # here = the whole inner dict for the current room.
        here = ROOMS[room]
        print()
        print(here["title"])
        print(here["text"])

        # Number the exits. targets[0] is exit 1, targets[1] is exit 2.
        # Start with empty lists, then fill both inside the loop below.
        targets = []
        valid = ["q"]                   # the answers we will accept
        for target in here["exits"]:    # a for loop over a dict gives its keys
            targets.append(target)
            # After the append, len(targets) is this exit's number (1, 2, ...).
            # Store it as TEXT, because input() gives text.
            valid.append(str(len(targets)))
            # here['exits'][target] is the words for this exit. Single quotes
            # inside, because the f-string itself uses double quotes.
            print(f"  {len(targets)}. {here['exits'][target]}")

        # INPUT -- validate with a while loop, as in P4LAB2
        answer = input("Pick a number, or q to quit: ").strip().lower()
        while answer not in valid:
            print("That is not on the list.")
            answer = input("Pick a number, or q to quit: ").strip().lower()

        # PROCESSING -- move: the number picks a room id out of targets
        # On "q" we skip the move, and the while test at the top ends the loop.
        if answer != "q":
            room = targets[int(answer) - 1]   # people count from 1, lists from 0

    print("You row home.")


# at the bottom -- start the program
main()
