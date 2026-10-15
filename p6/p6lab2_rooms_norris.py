# CTI 110
# P6LAB2 - Rooms as Data
# norris
# 11/5/26

# Three rooms, stored as DATA, not as functions.
# ROOMS is a dictionary. Each value is another dictionary (a dict of dicts).
# "exits" maps the id of the next room to the words the player sees.
# Read it, predict it, run it. Today we do not change it.

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
    answer = ""
    while answer != "q":
        # OUTPUT -- look up this room's dict, then show its title and text
        here = ROOMS[room]
        print()
        print(here["title"])
        print(here["text"])

        # Number the exits. targets[0] is exit 1, targets[1] is exit 2.
        targets = []
        valid = ["q"]                   # the answers we will accept
        for target in here["exits"]:    # a for loop over a dict gives its keys
            targets.append(target)
            valid.append(str(len(targets)))
            print(f"  {len(targets)}. {here['exits'][target]}")

        # INPUT -- validate with a while loop, as in P4LAB2
        answer = input("Pick a number, or q to quit: ").strip().lower()
        while answer not in valid:
            print("That is not on the list.")
            answer = input("Pick a number, or q to quit: ").strip().lower()

        # PROCESSING -- move: the number picks a room id out of targets
        if answer != "q":
            room = targets[int(answer) - 1]   # people count from 1, lists from 0

    print("You row home.")


# at the bottom -- start the program
main()
