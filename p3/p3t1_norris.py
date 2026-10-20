# CTI 110
# P3T1 - Warmup with If Statements
# norris
# 9/22/26

# WHAT THIS TEACHES
#   - Comparison operators: >=  ==  >  <=  !=  (and: == tests, = stores)
#   - if / elif / else: Python checks the tests in order, runs the FIRST
#     one that is true, and skips the rest.
#   - Nested if: a decision inside a decision.
#   - main(): wrap the program in a function, then call it at the bottom.
# Three small decisions, one ogre. The ogre has never lost a fight to
# a person who skipped the potions.

# main() -- this is the program's starting point.
# You don't need to use it, but it's a very good idea.
def main():
    # Part 1 - Level Check
    print("Hello and welcome to the dungeon.")
    level = int(input("What level are you? "))
    # >= means "greater than or equal to". Level 21 gets in. Level 20 does not.
    if level >= 21:
        print("You can enter the dragon's spire dungeon.")
    else:
        print("Try leveling up first.")

    # Part 2 - List your potions
    print("Time to enter the dungeon.")
    potions = int(input("How many health potions did you bring? "))
    # ORDER MATTERS. The tests run top to bottom and stop at the first true one.
    if potions == 0:
        print("It's dangerous to go alone without potions.")
    elif potions == 1:
        print(f"You have {potions} health potion.")    # singular: "potion"
    elif potions >= 1:
        # We reach this test only if potions is not 0 and not 1.
        # So ">= 1" is true here for 2 or more, and false for negatives.
        print(f"You have {potions} health potions.")   # plural: "potions"
    else:
        # Nothing above was true, so potions is below zero.
        print(f"How did you get {potions}??? that's less than zero")

    # Part 3 - Boss battle
    print ("You are facing the 👹DELUXE OGRE MAGE👹")
    print ("This will be a hard fight...")
    # Nested if: the second test happens only if the first one passes.
    if level >= 25:
        # You're tough enough to hit him...
        # "> 3" means 4 or more. Exactly 3 potions is NOT enough. (Careful:
        # > and >= differ by one, and that one is where bugs like to live.)
        if potions > 3:
            print("It takes three potions to get him to low health!")
            print("***YOU WIN***")
        else:
            print("You run out of healing before he's weakened.")
            print("***GAME OVER***")
    else:
        # This else pairs with "if level >= 25", because it lines up with it.
        print("His armor is too strong!")
        print("***GAME OVER***")


# at the bottom -- start the program
# Nothing runs until this line calls main(). def only teaches Python the name.
main()
