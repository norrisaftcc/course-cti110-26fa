# CTI 110
# P1HW1 - Math
# Norris, A
# 9/8/26
# Do some math processing

# PART 1 - EXPONENTS
print("-----Calculating Exponents-----")
print("\n") # 2 newlines
base = int(input("Enter integer as base value: "))
exponent = int(input("Enter integer as exponent: "))
result = base ** exponent  # example, (3 ** 2) is 3 squared
print(f"{base} to the {exponent} power is {result} !!")

# PART 2 - ADDITION SUBTRACTION
print("-----Addition and Subtraction-----")
print("\n") # 2 newlines
# 3 numbers, start, add_this, sub_this
start = int(input("Enter the starting integer: "))
#print("you typed", start)
add_this = int(input("Enter integer to add: "))
sub_this = int(input("Enter integer to subtract: "))
# Calculate the answer
answer = start + add_this - sub_this
# Print the answer
print()
print() # That gives 2 newlines, so would print("\n")
# Should look like: "10 + 4 - 2 is equal to 12"
print(start, "+", add_this, "-", sub_this, "is equal to", answer)
print(f"{start} + {add_this} - {sub_this} is equal to {answer}")
