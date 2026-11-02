# CTI 110
# P1LAB1
# Norris, A
# 9/1/26
# Our first Python program

# WHAT THIS TEACHES
#   - print() puts text on the screen.
#   - input() asks a question, waits, and hands back what the user typed.
#   - A variable is a name that holds a value: first_name = ...
#   - A comment starts with #. Python skips it. People should not.
# Every programmer has written this program. Yours is now on the list.

# First, we're going to greet the user
# Text goes inside quotes. The quotes are not printed.
print("Hello!")

# Next, ask their first name
#print("What's your name?")   # (old idea: a separate print, then input)
# input() prints the question, pauses, and returns the answer.
# The "=" does not mean "equals". It means "store the answer in this name".
# The answer is always a STRING (text), even if the user types digits.
first_name = input("What's your first name? ")

# do the same thing for last_name
last_name = input("What's your last name? ")

# Then say back the name
# Commas between items: print() puts one space between each item.
# That is why "Nice to meet you" needs no space at its end.
print("Nice to meet you", first_name, last_name)
