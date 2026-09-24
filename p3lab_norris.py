# CTI 110
# P3LAB - Making Change
# norrisa
# 9/24/26
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
cents = round(amount * 100) # convert to cents, round correctly
print("That's", cents,"cents.")

# For each currency type:
# - cents // [CURRENCY] gives you how many CURRENCY
# - cents % [CURRENCY] gives you the left over cents
dollars = cents // 100
cents   = cents % 100
# If statement - don't show of zero, use singular or plural otherwise
if dollars == 0:
    pass
if dollars == 1:
    print("1 dollar")
if dollars > 1:
    print(dollars,"dollars")
    
# quarters
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
pennies = cents
if pennies == 1:
    print("1 penny")
if pennies > 1:
    print(pennies, "pennies")

