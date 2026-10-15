# CTI 110
# P5LAB3 - Refactor
# norris
# 10/27/26

# EXAMPLE REVIEW NOTE (Rung 3: AI as reviewer, AFTER it worked and matched)
# Changed: nothing in the output. The AI said "pennies" should come
#   from count_coins too; I did that so all five coins use one pattern.
# Not changed: the AI wanted to fix the spacing in print("That's", ...).
#   I kept it. The output must match p3lab_norris.py byte for byte.

# REFACTOR of p3lab_norris.py (Making Change).
# The old file pasted the same coin block five times.
# Now the block is two functions. The output is EXACTLY the same.
# Prove it (run from the repo folder):
#   python3 p3lab_norris.py < p5/p5lab3_input.txt > before.txt
#   python3 p5/p5lab3_norris.py < p5/p5lab3_input.txt > after.txt
#   diff before.txt after.txt
# No output from diff means no difference.


# INPUT -- ask for dollars and cents, hand back whole cents
def get_cents():
    amount = float(input("Enter dollars and cents (ex: 2.91): "))
    cents = round(amount * 100)  # convert to cents, round correctly
    return cents


# PROCESSING -- how many coins of this size, and how many cents are left?
# Two return values, like tick(turn, torch) in P5LAB2.
def count_coins(cents, size):
    count = cents // size     # how many whole coins fit
    leftover = cents % size   # the cents that do not fit
    return count, leftover


# OUTPUT -- one line for one coin. Zero coins prints nothing.
def show_count(count, singular, plural):
    if count == 1:
        print("1", singular)
    if count > 1:
        print(count, plural)


def main():
    cents = get_cents()
    print("That's", cents,"cents.")   # spacing kept exactly as in P3LAB

    # Each coin: count it, keep the leftover, show the count
    dollars, cents = count_coins(cents, 100)
    show_count(dollars, "dollar", "dollars")

    quarters, cents = count_coins(cents, 25)
    show_count(quarters, "quarter", "quarters")

    dimes, cents = count_coins(cents, 10)
    show_count(dimes, "dime", "dimes")

    nickels, cents = count_coins(cents, 5)
    show_count(nickels, "nickel", "nickels")

    pennies, cents = count_coins(cents, 1)
    show_count(pennies, "penny", "pennies")


# at the bottom -- start the program
main()
