# _practice/practice.py
# A starter skeleton for a daily wellness tracker (water, exercise, produce).

# WHAT THIS TEACHES
#   - Top-down design: write the outline first. Name every function, leave
#     the bodies empty, and fill them in one at a time.
#   - "pass" is a placeholder. It means "do nothing, but this block is not
#     missing". Without it, an empty function is a syntax error.
#   - Parameters: each log_ function will receive a running total.
#   - The  if __name__ == "__main__"  guard: run main() only when this file
#     is the one being run, not when another file imports it.
# An outline that runs is better than a masterpiece that does not exist.
# Right now the only thing this program does is announce itself.


# main() is the starting point. For now it only proves the file runs.
def main():
    print("This is main")


# Shows the menu. Done already: it only prints, so nothing is left to decide.
def display_menu():
    # Show the main menu
    print("----MAIN MENU----")
    print("1. Log Water")
    print("2. Log Exercise Minutes")
    print("3. Log Fruit & Veggie Servings")
    print("4. View Daily Summary")
    print("5. Exit")


# TO DO: ask the user for a menu choice and return it.
def get_menu_choice():
    pass


# TO DO: fill these in. Each takes a running total as its parameter.
def log_water(total_water):
    pass


def log_exercise(total_exercise):
    pass


def log_servings(total_servings):
    pass


# __name__ is "__main__" only when you run this file directly.
if __name__ == "__main__":
    main()
