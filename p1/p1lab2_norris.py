# CTI 110
# P1LAB2 - Selling Things
# norrisa
# 9/3/26

# WHAT THIS TEACHES
#   - The three basic types: str (text), int (whole), float (decimal).
#   - input() always returns a str. To do math, convert it with int()/float().
#   - The shape of nearly every program: INPUT, then PROCESSING, then OUTPUT.
#   - Three ways to print a price. Only one of them is pleasant to write.
# Note: type "ten" where a number belongs and Python will stop with a
# ValueError. That is fair. "ten" is not a number to a computer.
# (p1/flask_demo/app.py shows how to catch that error politely.)

# Fictional Store -- pick three things
# product_name, product_count, product_price

# Hardcoding sets values directly.
# product_name = 'apples'   # strings use "quotes" and are made of text
# product_count = 100         # integers are whole numbers, no decimal
# product_price = 1.50       # floats are decimal numbers

# Instead, we ask the user with input()
# INPUT
print("STORE STARTUP")
print("_" * 10) # ten _ in a row  (str * int repeats the text)
product_name = input("Enter product name: ")
# These two are still TEXT here, even though the user typed digits.
product_count = input("Enter product count: ")
product_price = input("Enter unit price: ")

# PROCESSING
# Assigning to the same name replaces the old value: text becomes a number.
product_count = int(product_count)  # convert string to integer: "100" -> 100
product_price = float(product_price)# convert string to float: "3.25" -> 3.25
total = product_count * product_price # requires two numbers, returns a third number
# (Try it with the int() lines removed. "100" * "3.25" is a TypeError.)

# OUTPUT
print("CUSTOMER INTERFACE")
print("_" * 10) # ten _ in a row
print("Welcome to the", product_name, "store")
# For later -- f string with {variable:.2f} is the magic word to get 2 decimals
# Line 1 uses commas: each comma adds a space, so you get "$ 1.50" (a gap).
# Line 2 is an f-string: you place every character yourself, so "$1.50".
print("We have", product_count, product_name + "(s) at $", format(product_price, ".2f"), "each.")
print(f"We have {product_count} {product_name}(s) at ${product_price:.2f} each.")
# {total:.2f} means: show total as a float with 2 digits after the point.
print(f"Total is: ${total:.2f}.")
