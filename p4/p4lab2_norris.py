# CTI 110
# P4LAB2 - Loops
# norris
# 10/8/26

# WHAT THIS TEACHES
#   - for loop : repeat a known number of times, over a range or a list.
#   - while loop: repeat until a condition is false. Good for "ask again".
#   - Input validation: keep asking until the answer is acceptable.
#   - A loop inside a loop (nested): the for runs fully on each while pass.
#   - range(start, stop): STOP is not included. range(1, 13) is 1 to 12.
# Warmups first, then the real program. 99 bottles is a classic, and the
# song has never once ended early.

# warmups
# (This string is not run. It is a block comment. Take out the quotes
# and run each loop on its own to see what it prints.)
"""
for number in (1,2,3,4):
    print(number)
for number in range(5):
    print(number)
for beer in range(99, 0, -1):
    print(beer,"bottles of beer on the wall.")
# counting loop 
print ("7's times tables:")
for mult in range(1, 13):
    print (7 * mult)
"""

# Set up variables
# START THE MAIN LOOP
# The loop test needs a value BEFORE the first pass, so we set one.
# "yes" makes the loop run at least once.
again = "yes"
while again == "yes":
    # Ask the user for their chosen integer (0-12)
    multiplier = int(input("Enter a number 0-12: "))
    # validate (loop) - number must be between 0 and 12
    # "or": the answer is bad if it is too small OR too big.
    # The loop repeats until a good answer arrives, then falls through.
    while multiplier < 0 or multiplier > 12:
        print("That is not a valid answer.")
        multiplier = int(input("Enter a number 0-12: "))

    # print the times table header
    print("Multiplication Table")
    print("-"*20)
    # print the times table (loop)
    # range(1, 13) gives 1, 2, ... 12. The 13 is where it stops, not a value.
    for number in range(1, 13):
        #print(multiplier, "*", number, "=", number*multiplier)
        print(f"{multiplier} * {number} = {number * multiplier}")
    # Finally, ask if they want to repeat
    # The text is compared exactly: "Yes" or "y" ends the loop. (Why?)
    again = input("Run again? (yes/no) ")

# outside the loop
# This code is back at the left margin, so it runs once, after the loop ends.
print()
print("Exiting program...")
