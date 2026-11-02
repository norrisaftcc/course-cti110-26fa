# CTI 110
# P5LAB - Purchase and change
# norrisa
# 10/29/26
# Self checkout machine simulator. Makes change.

# WHAT THIS TEACHES
#   - A function with a PARAMETER and NO return value. It receives the
#     amount, prints what it needs to, and hands nothing back.
#   - Reuse. The P3LAB coin-counting code becomes a function, so main()
#     can call it with any amount.
#   - The random module: random.uniform(low, high) gives a random float.
#   - main() as the table of contents: the sale, the payment, the change.
#   - Money is slippery. Subtracting two prices gives a float that may be a
#     hair off (see the note in main). P3LAB solved it with round().
# This file is a SKELETON. The marked TO DO is your work. Run it first:
# it already works, in the way a self-checkout works before it is stocked.
import random # required for random.uniform()

# Put other functions here.
# Turn the program P3LAB into a function called disperse_change. It should take one float parameter and have no return value.
def disperse_change(amount):
    # Print out the change needed.
    # Input: float
    # Return: nothing
    # (A function with no return line gives back None, Python's "nothing".)
    print(f"Change is: ${amount:.2f}")
    print()
    # Put your P3LAB code here: Print the number of dollars, quarters, dimes, nickels, pennies.
    # TO DO. Hint from P3LAB: work in whole cents, so convert first.
    # A float is not exact. Paying $5.00 for a $0.11 item gives change of
    # 4.89, and 4.89 * 100 is really 488.99999999999994. int() chops that to
    # 488, a cent short. round() gives the 489 you meant.

# Main
def main():
    # Declare variables
    # Python does not need these lines. They only give each name a starting
    # value and tell the reader what the program will use.
    cost = 0.0
    amount_paid = 0.0
    change_owed = 0.0
    print("Welcome to the self-checkout sim.")
    # Generate a random float value for the cost - uniform picks a number in this range
    # round(x, 2) keeps two decimals, because prices have cents and no more.
    cost = round(random.uniform(0.01, 100.00), 2)
    print(f"You owe: ${cost:.2f}")
    # Ask the user how much $ they put in
    amount_paid = float(input("How much money do you put in the self checkout? $"))
    # Calc change owed
    # Nothing checks that amount_paid covers the cost. Pay too little and
    # the change comes out negative. The machine is trusting. Real ones
    # are not.
    change_owed = amount_paid - cost

    print("Here is your change:")
    # Call the function and pass it the amount. There is nothing to catch
    # on the left of the call, because disperse_change returns nothing.
    disperse_change(change_owed)



# Last line - start the program
main()
