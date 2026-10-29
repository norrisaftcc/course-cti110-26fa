# CTI 110
# P5LAB - Purchase and change
# norrisa
# 10/29/26
# Self checkout machine simulator. Makes change.
import random # required for random.uniform()

# Put other functions here.
# Turn the program P3LAB into a function called disperse_change. It should take one float parameter and have no return value.
def disperse_change(amount):
    # Print out the change needed.
    # Input: float
    # Return: nothing
    print(f"Change is: ${amount:.2f}")
    print()
    # Put your P3LAB code here: Print the number of dollars, quarters, dimes, nickels, pennies.

# Main 
def main():
    # Declare variables
    cost = 0.0
    amount_paid = 0.0
    change_owed = 0.0
    print("Welcome to the self-checkout sim.")
    # Generate a random float value for the cost - uniform picks a number in this range
    cost = round(random.uniform(0.01, 100.00), 2)
    print(f"You owe: ${cost:.2f}")
    # Ask the user how much $ they put in
    amount_paid = float(input("How much money do you put in the self checkout? $"))
    # Calc change owed
    change_owed = amount_paid - cost
    
    print("Here is your change:")
    disperse_change(change_owed)



# Last line - start the program
main()