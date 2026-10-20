# CTI 110
# P2LAB2 - Dictionaries
# norrisa
# 9/15/26

# WHAT THIS TEACHES
#   - A dictionary stores pairs: a KEY you look up, and the VALUE it gives.
#   - cars["Prius"] finds the value for the key "Prius". No searching by hand.
#   - Use the looked-up value in a formula (miles / mpg = gallons).
#   - Keys must match exactly. Type "prius" and the program crashes with a
#     KeyError. The dictionary is not rude. It is just literal.
# (A later lab shows how to check first with:  if car in cars: )

# Car dictionary that lets us look up mpg
# From that mpg, find gallons burned per X miles.

# key : value, separated by commas. The braces { } make a dictionary.
cars = {
    "Camaro": 18.21,
    "Prius" : 52.36,
    "Model S" : 110,
    "Silverado" : 26,
}
print(cars)
# .keys() lists only the keys. It prints as dict_keys([...]).
car_keys = cars.keys()
print(car_keys)
# Choose the car
car = input("Enter a vehicle to see its mpg: ")
# Look up by key. Capital letters must match the dictionary exactly.
mpg = cars[car]
print(f"The MPG of a {car} is {mpg} miles per gallon.")
# Ask user for miles, output gas used
miles = float(input(f"How many miles will you drive the {car}? "))
gallons_used = miles / mpg # miles divided by miles per gallon gives units in gallons
print(f"Driving a {car} for {miles} miles will use {gallons_used:.2f} gallons of gas.")
