# CTI 110
# P2HW2 - just the setup

# This example only uses three numbers, the full uses six.
# Get the grades
grade1 = float(input("Enter grade #1: "))
grade2 = float(input("Enter grade #2: "))
grade3 = float(input("Enter grade #3: "))
# Put them all into a new list
grade_list = [grade1, grade2, grade3]

# Do some calculations -- minimum, maximum, and average
min_grade = min(grade_list)
max_grade = max(grade_list)
total     = sum(grade_list)
count     = len(grade_list)
# TODO: calc average (total / count)

# Print the output
print(f"Grades: {grade_list}")
print(f"Lowest: {min_grade}")
# print the rest of the output (TODO)
