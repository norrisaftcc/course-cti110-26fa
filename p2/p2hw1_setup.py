# CTI 110
# P2HW1 - Setup Only
# Talk about how to format the display

# WHAT THIS TEACHES
#   - Lining up a label column and a value column with f-string widths.
#   - {text:<15} means: left-align in a field 15 characters wide.
#   - {number:<15.2f} adds: show as a float with 2 decimals.
#   - A dollar sign OUTSIDE the braces is just text, printed as it is.
# Run it and the colons line up like soldiers. Change one 15 and watch the
# column fall apart. That is the lesson.
# NOTE: quotes inside an f-string's braces may match the outer quotes only
# in Python 3.12 or newer. On an older Python, use single quotes inside.

# Sample data - real program uses input()
destination = "Raleigh"
budget      = 2000
expenses    = 1000
remaining   = budget - expenses   # the program does the subtraction, not you

# Each label is a string literal placed inside the braces, so it gets a width
# too. Same width (15) on every row is what makes the values line up.
print(f"{"Destination:":<15} {destination:<15}")
# budget is an int, but the .2f format shows it as 2000.00. No int() needed.
print(f"{"Budget:":<15} ${budget:<15.2f}")
print(f"{"Expenses:":<15} ${expenses:<15.2f}")
print(f"{"Remaining:":<15} ${remaining:<15.2f}")
