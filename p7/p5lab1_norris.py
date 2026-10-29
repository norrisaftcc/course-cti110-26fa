# CTI 110
# P5LAB1 - Functions
# norris
# 10/20/26

# AFTER: the same walk as p5lab1_before_norris.py, now with functions.
# Each pasted block gets a name with def. Then we call it by name.
# The output is exactly the same as the before file. Check it with diff.

# def makes a function. Nothing runs yet. Python just learns the name.
def show_divider():
    # The divider and banner. Written once, used three times.
    print()
    print("=" * 40)
    print("THE FIRST DELVE")
    print("=" * 40)


def show_help():
    # The help block. Written once, used three times.
    print("- Light is time. The torch is a clock you can see.")
    print("- Searching finds things, and it costs a turn.")
    print("- Listen before you open a door. Forcing it makes noise.")


def describe_docks():
    print("The Fort docks. Captain Maren coils a wet rope and does not smile.")
    print("\"Row to the Isle of Old Stone. Find out who lands there,")
    print("and what moves in the water.\"")


def describe_jetty():
    print("S1. THE BROKEN JETTY")
    print("A stone jetty runs out from the south shore. Half of it has fallen")
    print("into the lake. On a mooring post, a rope burn shows pale and fresh:")
    print("someone else lands here.")


def describe_tower():
    print("S2. THE TOWER SHELL")
    print("A round tower, thirty feet across, open to the sky. Its upper floors")
    print("fell in long ago and lie as rubble on the ground.")


# main() is the program's starting point. It reads like a table of contents.
def main():
    # INPUT
    name = input("What is your hero's name? ")
    print(f"Hero: {name}")

    # OUTPUT -- each line is a call: the name, then ()
    show_divider()
    describe_docks()
    show_help()

    show_divider()
    describe_jetty()
    show_help()

    show_divider()
    describe_tower()
    show_help()


# at the bottom -- start the program
main()
