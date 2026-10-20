"""
(block comments -- continue until the triple quotes end)
CTI 110
P2LAB1
norrisa
9/15/26
Get Radius, calculate and display diameter, circumference, and area
"""
# WHAT THIS TEACHES
#   - A constant: a name in CAPITAL LETTERS that you promise not to change.
#   - Math with variables: formulas in code look like formulas on paper.
#   - Rounding on display only: .1f, .2f and .3f change what is SHOWN,
#     not the number that is stored.
#   - float(input(...)): ask for a number that may have decimals.
# Archimedes worked on this problem for years. You get it in ten lines.

# Python does not enforce constants. Capitals are a signal to other people.
PI = 3.14159 # Constant - do not change
# Input -- get radius
radius = float(input("What is the radius of the circle? "))

# Calculation -- find diameter, circumference, and area
# diameter = 2*r, circumference = 2*pi*r, area = pi*r*r
diameter = 2 * radius
circumference = 2 * PI * radius
area = PI * radius * radius

# Output -- .1f, .2f, .3f
# Same idea three times, to show the digit after the point changes the output.
print(f"The diameter is {diameter:.1f}")
print(f"The circumference is {circumference:.2f}")
print(f"The area is {area:.3f}")
