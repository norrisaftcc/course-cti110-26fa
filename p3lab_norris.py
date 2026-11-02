# CTI 110
# P3LAB - Making Change
# norrisa
# 9/24/26

# WHAT THIS TEACHES
#   - Floor division //  : how many whole times does B fit in A?  (7 // 2 is 3)
#   - Modulus %          : what is left over after that?          (7 % 2 is 1)
#   - Together they split an amount into coins, largest coin first.
#   - if statements that stay silent for zero, and pick singular or plural.
#   - Why money is counted in whole cents, not in decimals (see below).
# The cashier in your head does this all day. Now the computer can, too.
# (P5LAB3 later cleans this file up. Count how many times the same block
# is pasted. That number is the homework for next month.)

# Example 1 below is a warm-up inside a triple-quoted string. Python reads
# it as text and runs none of it, so it works like a block comment.
# Same math as the coins, with potions instead.
"""
# Example 1 -- with potions
hp = int(input("How many hit points of damage (1-100): "))
print("You took ", hp, "Damage!")

# Large potions heal 25
large = hp // 25        # each potion heals 25
hp    = hp % 25         # some damage left over

print("Drank ", large, "large potions.")
print("Damage remaining: ", hp)

# Small potions heal 5
small = hp // 5
hp    = hp % 5

print("Drank", small, "small potions.")
print("Damage remaining: ", hp)
"""
# Example 2 - With Coins
amount = float(input("Enter dollars and cents (ex: 2.91): "))
# Why round()? Decimals are stored in binary, which is close but not exact:
#   0.29 * 100 is really 28.999999999999996
# int() would chop that to 28 cents. round() gives the 29 we meant.
cents = round(amount * 100) # convert to cents, round correctly
print("That's", cents,"cents.")

# For each currency type:
# - cents // [CURRENCY] gives you how many CURRENCY
# - cents % [CURRENCY] gives you the left over cents
# The order matters: take the biggest coin first, then pass the leftover on.
dollars = cents // 100
cents   = cents % 100
# If statement - don't show if zero, use singular or plural otherwise
# (1 gets "dollar", more than 1 gets "dollars", 0 prints nothing at all)
if dollars == 0:
    pass     # "pass" means do nothing. Python needs SOME line in the block.
if dollars == 1:
    print("1 dollar")
if dollars > 1:
    print(dollars,"dollars")

# quarters
# 'cents' now holds only what the dollars left behind (0 to 99).
quarters = cents // 25
cents    = cents % 25
if quarters == 0:
    pass
if quarters == 1:
    print("1 quarter")
if quarters > 1:
    print(quarters,"quarters")

# dimes
dimes = cents // 10
cents = cents % 10
if dimes == 1:
    print("1 dime")
if dimes > 1:
    print(dimes, "dimes")

# nickels
nickels = cents // 5
cents = cents % 5
if nickels == 1:
    print("1 nickel")
if nickels > 1:
    print(nickels, "nickels")

# pennies
# Whatever is left after nickels IS the penny count. No division needed.
pennies = cents
if pennies == 1:
    print("1 penny")
if pennies > 1:
    print(pennies, "pennies")
