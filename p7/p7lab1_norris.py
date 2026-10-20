# CTI 110
# P7LAB1 - Dispatch Loop
# norris
# 11/10/26

# P5LAB2 rooms, one step further.
# 1. hero is a DICTIONARY: a character sheet with name, role, hp and items.
#    (Refresher: p2/p2lab2_norris.py used a dict; p2/p2hw2_setup.py a list.)
# 2. ROOMS is a dictionary of FUNCTIONS. It replaces the if/elif chain.
#    room = ROOMS[room](hero) looks up the function, then calls it.
# 3. The LEVER: the docks ask Fighter or Wizard. Later rooms test hero["role"].

# WHAT THIS TEACHES
#   - Functions are VALUES. You can store one in a dict and call it later.
#   - A dispatch table: look up the right function by name, then call it.
#     It replaces a long if/elif chain, and it does not grow when rooms do.
#   - A mutable dict passed to a function is the SAME dict. If a room
#     changes it, main() sees the change. No return is needed for that.
#     (The room still returns the next room id. That is a different job.)
#   - A story "lever": an early choice that changes what is possible later.
#     The wizard who skipped the cottage meets a stuck door. Choices cost.
# Five giant rats wait at the end. They have been very patient.


# ask() shows a prompt and returns the answer, trimmed and in lower case
def ask(prompt):
    return input(prompt).strip().lower()


# Ask until the answer is one of the choices in the list
def ask_choice(prompt, choices):
    answer = ask(prompt)
    while answer not in choices:
        print("That is not one of the choices. Try again.")
        answer = ask(prompt)
    return answer


# Each room takes the hero dict and RETURNS the next room id (or "end").
# A room may change the dict: hero["role"] = ..., hero["items"].append(...)
# Every room takes hero, even one that does not use it (like jetty). The
# dispatch loop calls them all the same way, so they must all fit the same shape.
def docks(hero):
    print()
    print("The Fort docks. Captain Maren coils a wet rope and does not smile.")
    print("Who rows to the island?")
    print("  1. The Fighter: 8 hit points")
    print("  2. The Wizard: 4 hit points")
    pick = ask_choice("Pick 1 or 2: ", ["1", "2"])
    # THE LEVER: an early choice, stored as a field on the character sheet
    # Assigning to a key changes the caller's dict. We do not need to return it.
    if pick == "1":
        hero["role"] = "fighter"
        hero["hp"] = 8
    else:
        hero["role"] = "wizard"
        hero["hp"] = 4
    print(f"{hero['name']} is the {hero['role']}, with {hero['hp']} hit points.")
    return "jetty"


def jetty(hero):
    print()
    print("S1. THE BROKEN JETTY")
    print("Half the jetty lies in the lake. A rope burn on a post is fresh.")
    print("  1. Walk up to the tower")
    print("  2. Row home")
    if ask_choice("Pick 1 or 2: ", ["1", "2"]) == "1":
        return "tower"
    return "end"


def tower(hero):
    print()
    print("S2. THE TOWER SHELL")
    print("Rubble covers the floor. Under the rubble lies a trapdoor of black oak.")
    print("  1. Walk down to the jetty")
    print("  2. Look in the cottage")
    print("  3. Go down through the trapdoor")
    pick = ask_choice("Pick 1, 2 or 3: ", ["1", "2", "3"])
    if pick == "1":
        return "jetty"
    elif pick == "2":
        return "cottage"
    return "cellar"


def cottage(hero):
    print()
    print("S3. THE KEEPER'S COTTAGE")
    print("No roof. Ash in the hearth, less than a week old. A tin of lamp oil.")
    # Only offer the oil once: test the items list with "in"
    # "not in" is True when the list does not hold the item yet.
    if "oil" not in hero["items"]:
        if ask_choice("Take the lamp oil? (y/n): ", ["y", "n"]) == "y":
            # .append() changes the list inside hero. main() will see it.
            hero["items"].append("oil")
            print("You take the oil.")
    return "tower"


def cellar(hero):
    print()
    print("C1. THE CELLAR STAIR")
    print("At the bottom stands an oak door, swollen in its frame. It is stuck.")
    # THE LEVER again: the same door, a different way through for each role
    # The menu text changes with the hero. The outcomes below must match it.
    if hero["role"] == "fighter":
        print("  1. Force the door (Fighter)")
    elif "oil" in hero["items"]:
        print("  1. Oil the hinges and ease the door open (Wizard, with oil)")
    else:
        print("  1. Push the door (Wizard, no oil)")
    print("  2. Climb back to the tower")
    if ask_choice("Pick 1 or 2: ", ["1", "2"]) == "2":
        return "tower"
    if hero["role"] == "fighter":
        print("The door bursts open with a crack like a dropped plank.")
        return "store"
    if "oil" in hero["items"]:
        print("The oiled door swings open without a sound.")
        return "store"
    print("The door will not move. Oil from the cottage might help.")
    # Returning "cellar" sends the hero here AGAIN, through the main loop.
    # It is a loop, not a function calling itself, so the pile stays flat.
    return "cellar"


def store(hero):
    print()
    print("C2. THE OIL STORE")
    print("Racks of broken oil jars. The floor is tacky.")
    print("Five giant rats, each the size of a cat, lift their heads from the spill.")
    print("You back up the stair. The rats do not follow.")
    return "end"


# A dict of FUNCTIONS. No () here: we store the function, we do not call it.
# Write docks() and Python RUNS it. Write docks and Python just holds it.
# Each key is the same room id that the rooms return.
ROOMS = {
    "docks": docks,
    "jetty": jetty,
    "tower": tower,
    "cottage": cottage,
    "cellar": cellar,
    "store": store,
}


def show_sheet(hero):
    print()
    print("CHARACTER SHEET")
    print(f"Name:  {hero['name']}")
    print(f"Role:  {hero['role']}")
    print(f"HP:    {hero['hp']}")
    print(f"Items: {hero['items']}")


def main():
    # INPUT -- start the character sheet. docks() fills in role and hp.
    name = input("What is your hero's name? ").strip()
    # Empty values now; the rooms fill them in as the story goes on.
    hero = {"name": name, "role": "", "hp": 0, "items": []}

    # PROCESSING -- the dispatch loop. Look up the room, call it, save the id.
    # Read the one line from the inside out:
    #   ROOMS[room]        -> the function for this room id
    #   ROOMS[room](hero)  -> call it, passing the character sheet
    #   room = ...         -> keep what it returns: the next room id
    # A misspelled room id would raise a KeyError here. That is useful: it
    # stops the game at once and names the bad id.
    room = "docks"
    while room != "end":
        room = ROOMS[room](hero)

    # OUTPUT
    show_sheet(hero)


# at the bottom -- start the program
main()
