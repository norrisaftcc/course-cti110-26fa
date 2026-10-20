# CTI 110
# P6LAB1 - Tutor Check
# norris
# 11/3/26

# This program has ONE bug in it, on purpose.
# It runs. It does not crash. But the last line it prints is wrong.
#
# What to do:
#   1. Run it:  python3 p6lab1_tutor_check.py
#   2. Read the last line it prints.
#   3. Do NOT fix it first. Ask your AI tutor:
#          Why does this print None?
#   4. Fill in the checklist on the P6LAB1 sheet.
#   5. Then fix it yourself. The fix is one line.

# WHAT THIS TEACHES
#   - How to use an AI tutor well: ask a precise question, check its answer
#     against the code, and then do the fix with your own hands.
#   - How to debug a program that runs but is wrong. No crash, no error
#     message. Only a wrong answer. These are the hard bugs.
#   - Reading a program by FOLLOWING A VALUE: where is it made, where does
#     it go, and what arrives at the end?
# The comments below describe the code. They do not point at the bug.
# Finding it is the exercise. (It is not hiding. It is just quiet.)


# get_scores() hands back a list of four quiz scores.
# They are typed in here, so everyone in the class sees the same output.
def get_scores():
    scores = [88, 92, 75, 100]
    return scores


# average() adds up the numbers, then divides by how many there are.
def average(numbers):
    total = 0
    # A for loop visits each number in the list, one at a time.
    for number in numbers:
        total = total + number
    result = total / len(numbers)
    print("Inside average(), the result is", result)


# main() reads like a table of contents for the program.
def main():
    # Step 1: get the scores. Step 2: find the average. Step 3: show both.
    scores = get_scores()
    print("Scores:", scores)
    avg = average(scores)
    print("Average:", avg)


main()
