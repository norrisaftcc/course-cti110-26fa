# norrisa
# 10/27/26
# P5T: The Potion Pouch
# This is the potion ritual from The Changekeeper (Potions tab).
# It is the same // and % pattern as your P3LAB, with two potions:
#   Large Potion heals 25 HP. Small Potion heals 5 HP.
# Run it now (it works). In P5T you turn it into a function.

# WHAT THIS TEACHES (this is the finished P5T; the starter is P5T_starter.py)
#   - Turning a script into a function. The potion code is the same as the
#     starter's. It now has a name, a parameter, and a place to be called from.
#   - Two kinds of function, side by side:
#       drink_potions(hp_missing)  PRINTS its result and returns nothing.
#       get_random_gold()          RETURNS its result and prints nothing.
#   - The random module: randint(a, b) picks a whole number, and BOTH ends
#     are possible. uniform(a, b) picks a float.
#   - main() ties it together: a goblin hits, you drink, you loot a chest.
# The goblin is not a threat. The goblin is a random number generator
# in a small hat.

import random

# hp_missing is a PARAMETER: main() hands in the number.
def drink_potions(hp_missing):
    # input: hp_missing -> max healing possible
    # output: prints potions used
    # Same math as the starter. The // counts potions, the % keeps the rest.
    # (Changing hp_missing here changes only this function's copy. The
    # caller's number is untouched.)
    large = hp_missing // 25
    hp_missing = hp_missing % 25
    if large == 1:
        print(large, "Large Potion")
    elif large > 1:
        print(large, "Large Potions")

    small = hp_missing // 5
    hp_missing = hp_missing % 5
    if small == 1:
        print(small, "Small Potion")
    elif small > 1:
        print(small, "Small Potions")

    print("Still missing:", hp_missing, "HP")

def get_random_gold():
    # Returns a float -- how much gold was found
    # uniform() gives a float in the range. round(..., 2) trims it to cents.
    gold = round(random.uniform(0.01, 100.00), 2)
    # return sends the value back to whoever called. main() will catch it.
    return gold


def main():
    #hp_missing = int(input("Enter HP missing: "))
    #drink_potions(hp_missing)
    # (The two lines above are the starter's way: the player types the damage.
    # Below, the program makes up the damage. Same function, new caller.)
    max_hp = int(input("What is your max HP? "))
    # randint(1, max_hp) can give 1 or max_hp. A max HP below 1 makes the
    # range empty, and randint raises a ValueError.
    hp = random.randint(1, max_hp)
    print(f"A goblin hits you. You have {hp} HP left.")
    hp_missing = max_hp - hp
    print(f"You are missing {hp_missing} HP.")
    drink_potions(hp_missing)

    # get random gold
    # The call runs the function and the answer lands in gold.
    gold = get_random_gold()
    print(f"You find {gold:.2f} gold in the chest.")



# Start the program
main()
