# CTI 110
# P1HW1 - Math
# Norris, A
# 9/8/26
# Do some math processing

# WHAT THIS TEACHES
#   - int(input(...)): ask, then convert the answer to a whole number.
#   - Math operators: ** (power), + (add), - (subtract).
#   - Two ways to print a mix of text and numbers: commas, or an f-string.
#   - Order of work: Python does the inside call first, then the outside.
# Spoiler: both print styles give the same output here. Pick the one that
# hurts your eyes less. (Most people pick the f-string.)

# PART 1 - EXPONENTS
print("-----Calculating Exponents-----")
print("\n") # 2 newlines
# Read inside-out: input() runs first and returns TEXT. Then int() turns
# that text into a number. Type "abc" and int() raises a ValueError.
base = int(input("Enter integer as base value: "))
exponent = int(input("Enter integer as exponent: "))
result = base ** exponent  # example, (3 ** 2) is 3 squared
# In an f-string, anything inside {} is replaced by its value.
print(f"{base} to the {exponent} power is {result} !!")

# PART 2 - ADDITION SUBTRACTION
print("-----Addition and Subtraction-----")
print("\n") # 2 newlines
# 3 numbers, start, add_this, sub_this
start = int(input("Enter the starting integer: "))
#print("you typed", start)   # a handy debug trick: print what you got
add_this = int(input("Enter integer to add: "))
sub_this = int(input("Enter integer to subtract: "))
# Calculate the answer
# + and - work left to right, so this is (start + add_this) - sub_this
answer = start + add_this - sub_this
# Print the answer
print()
print() # That gives 2 newlines, so would print("\n")
# Should look like: "10 + 4 - 2 is equal to 12"
# Style 1: commas. print() adds a space between items. Quotes mark the text.
print(start, "+", add_this, "-", sub_this, "is equal to", answer)
# Style 2: f-string. Same output. You control every character.
print(f"{start} + {add_this} - {sub_this} is equal to {answer}")
