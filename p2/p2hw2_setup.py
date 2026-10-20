# CTI 110
# P2HW2 - just the setup

# WHAT THIS TEACHES
#   - A list holds many values under one name: [88.0, 92.5, 75.0]
#   - Built-in functions do the heavy work: min(), max(), sum(), len().
#   - Average = total / count. The two numbers come from sum() and len().
#   - Collect the data first, then calculate, then print. Three tidy steps.
# The TODO marks are the homework. This file is the part we hand you for
# free. Enjoy it. It is the only free part.

# This example only uses three numbers, the full uses six.
# Get the grades
# float() because grades may have decimals (87.5). input() gives text.
grade1 = float(input("Enter grade #1: "))
grade2 = float(input("Enter grade #2: "))
grade3 = float(input("Enter grade #3: "))
# Put them all into a new list
# Square brackets make a list. The items keep the order you put them in.
grade_list = [grade1, grade2, grade3]

# Do some calculations -- minimum, maximum, and average
# Each of these takes the whole list and returns ONE number.
min_grade = min(grade_list)
max_grade = max(grade_list)
total     = sum(grade_list)
count     = len(grade_list)   # len() counts the items, so it works for 3 or 6
# TODO: calc average (total / count)

# Print the output
# Printing a list shows it as it is written: [88.0, 92.5, 75.0]
print(f"Grades: {grade_list}")
print(f"Lowest: {min_grade}")
# print the rest of the output (TODO)
