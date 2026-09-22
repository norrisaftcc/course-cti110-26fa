# CTI 110
# P3T1 - Warmup with If Statements
# norris
# 9/22/26

# main() -- this is the program's starting point.
# You don't need to use it, but it's a very good idea.
def main():
    # Part 1 - Level Check
    print("Hello and welcome to the dungeon.")
    level = int(input("What level are you? "))
    if level >= 21:
        print("You can enter the dragon's spire dungeon.")
    else:
        print("Try leveling up first.")

    # Part 2 - List your potions
    print("Time to enter the dungeon.")
    potions = int(input("How many health potions did you bring? "))
    if potions == 0:
        print("It's dangerous to go alone without potions.")
    elif potions == 1:
        print(f"You have {potions} health potion.")
    elif potions >= 1:
        print(f"You have {potions} health potions.")
    else: 
        print(f"How did you get {potions}??? that's less than zero")

    # Part 3 - Boss battle
    print ("You are facing the 👹DELUXE OGRE MAGE👹")
    print ("This will be a hard fight...")
    if level >= 25:
        # You're tough enough to hit him...
        if potions > 3:
            print("It takes three potions to get him to low health!")
            print("***YOU WIN***")
        else:
            print("You run out of healing before he's weakened.")
            print("***GAME OVER***")
    else:
        print("His armor is too strong!")
        print("***GAME OVER***")
    

# at the bottom -- start the program
main()
