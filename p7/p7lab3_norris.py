# CTI 110
# P7LAB3 - Save File
# norris
# 11/17/26

# A program can stop and start again where it left off.
# We save the character sheet (a dict) to a JSON file, then load it back.
# Run this from inside the p7 folder: cd p7. It writes hero_save.json there.

import json


# Write the hero dict to a file. indent=2 makes the file easy to read.
# "w" means write: it makes the file, or replaces what was in it.
def save_hero(hero, path):
    with open(path, "w") as save_file:
        json.dump(hero, save_file, indent=2)


# Read the file back. json.load turns the text into a dict again.
def load_hero(path):
    with open(path, "r") as save_file:
        return json.load(save_file)


def main():
    # A character sheet. items and flags are LISTS, so JSON can save them.
    hero = {
        "name": "Brann",
        "role": "fighter",
        "hp": 8,
        "items": ["torch", "oil"],
        "flags": ["door_open", "lamp"],   # a sorted list, never a set
    }

    # PROCESSING -- save, then load into a NEW variable
    save_hero(hero, "hero_save.json")
    loaded = load_hero("hero_save.json")

    # OUTPUT -- the two dicts should hold exactly the same things
    print("Saved: ", hero)
    print("Loaded:", loaded)
    print("hero == loaded:", hero == loaded)


# THE TRAP: a set cannot be saved as JSON.
# A set looks handy for flags: no repeats, fast "in". But try it:
#
#   flags = {"lamp"}
#   json.dump({"flags": flags}, open("bad.json", "w"))
#
# Python stops with:
#   TypeError: Object of type set is not JSON serializable
#
# JSON has lists, but it has no sets. THE FIX: save a sorted list.
#
#   json.dump({"flags": sorted(flags)}, open("good.json", "w"))
#
# sorted() turns the set into a list, in the same order every time.
# That is why the kit keeps flags as a sorted list.


# at the bottom -- start the program
main()
