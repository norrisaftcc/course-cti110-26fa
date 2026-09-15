"""
(block comments -- continue until the triple quotes end)
CTI 110
P2LAB1
norrisa
9/15/26
Get Radius, calculate and display diameter, circumference, and area
"""
PI = 3.14159 # Constant - do not change
# Input -- get radius
radius = float(input("What is the radius of the circle? "))

# Calculation -- find diameter, circumference, and area
# diameter = 2*r, circumference = 2*pi*r, area = pi*r*r
diameter = 2 * radius
circumference = 2 * PI * radius
area = PI * radius * radius 

# Output -- .1f, .2f, 3.f 
print(f"The diameter is {diameter:.1f}")
print(f"The circumference is {circumference:.2f}")
print(f"The area is {area:.3f}")
