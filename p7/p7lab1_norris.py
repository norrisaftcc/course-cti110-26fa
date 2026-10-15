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
def docks(hero):
    print()
    print("The Fort docks. Captain Maren coils a wet rope and does not smile.")
    print("Who rows to the island?")
    print("  1. The Fighter: 8 hit points")
    print("  2. The Wizard: 4 hit points")
    pick = ask_choice("Pick 1 or 2: ", ["1", "2"])
    # THE LEVER: an early choice, stored as a field on the character sheet
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
    if "oil" not in hero["items"]:
        if ask_choice("Take the lamp oil? (y/n): ", ["y", "n"]) == "y":
            hero["items"].append("oil")
            print("You take the oil.")
    return "tower"


def cellar(hero):
    print()
    print("C1. THE CELLAR STAIR")
    print("At the bottom stands an oak door, swollen in its frame. It is stuck.")
    # THE LEVER again: the same door, a different way through for each role
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
    return "cellar"


def store(hero):
    print()
    print("C2. THE OIL STORE")
    print("Racks of broken oil jars. The floor is tacky.")
    print("Five giant rats, each the size of a cat, lift their heads from the spill.")
    print("You back up the stair. The rats do not follow.")
    return "end"


# A dict of FUNCTIONS. No () here: we store the function, we do not call it.
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
    hero = {"name": name, "role": "", "hp": 0, "items": []}

    # PROCESSING -- the dispatch loop. Look up the room, call it, save the id.
    room = "docks"
    while room != "end":
        room = ROOMS[room](hero)

    # OUTPUT
    show_sheet(hero)


# at the bottom -- start the program
main()
