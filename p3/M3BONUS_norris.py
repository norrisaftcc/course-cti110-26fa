# Your Name
# Date
# M3BONUS - Let's Make a Deal
# A short text adventure. The player picks a door and wins a prize.

"""
PSEUDOCODE
Display the welcome banner
Ask the player to pick door 1, 2, or 3
If the player picks 1: go to the goat room
Else if the player picks 2: go to the car room
Else if the player picks 3: go to the briefcase room
Else: the host says that is not a door
"""


def door_1():
    print()
    print("Door 1 swings open.")
    print("A goat looks at you. It is chewing your ticket.")
    print("You win: one goat.")


def door_2():
    print()
    print("Door 2 swings open.")
    print("Lights flash. A small red car rolls out.")
    print("You win: a car.")


def door_3():
    print()
    print("Door 3 swings open.")
    print("A briefcase sits on a stool.")
    print("You win: the briefcase.")
    # TO DO (Part C): start the Buzzer Round from here.
    print("BONUS BUZZER ROUND")
    max_time = 60
    base_winnings = 0
    bonus = 0
    print("Buzz in when you know the answer!")
    print("$10 per second left when you buzz in.")
    print("1.5 Multiplier if you have more than 40 seconds left!")
    time_used = float(input("How many seconds out of 60 do you need to get the answer? "))

    time_left = max_time - time_used
    # BONUS: If you have more than 40 seconds left you get 1.5 payout
    # Otherwise, you get 1.0 payout ($10 per second left)
    # Base case: up to $10 times 40 seconds
    # Bonus case: the base case, plus $15 for each extra second left over 40
    
    if time_left > 40:
        base_winnings = 40 * 10     # base caps at 40 seconds
        bonus_time = time_left - 40 # we already paid for the 40 seconds
        bonus =  bonus_time * 15    # bonus pays time and a half, or $15
    else:
        base_winnings = time_left * 10
        bonus_time = 0
        bonus = 0

    # TODO: f-string display of the prize and details
    # Testing with 20 chars on left, 10 on right
    print(f"{'Prize won:':<20}{'Briefcase':<10}")
    print(f"{'Time left:':<20}{time_left:<10}")
    print(f"{'Base prize:':<20}${base_winnings:<10.2f}")
    print(f"{'Bonus:':<20}${bonus:<10.2f}")

    



def start():
    print("=" * 40)
    print("     WELCOME TO LET'S MAKE A DEAL")
    print("=" * 40)
    choice = input("Pick a door (1, 2, or 3): ")

    if choice == "1": 
        door_1()
    elif choice == "2":
        door_2()
    elif choice == "3":
        door_3()
    else:
        print("The host frowns. That is not a door.")


# This line starts the game. Leave it at the bottom of the file.
start()
