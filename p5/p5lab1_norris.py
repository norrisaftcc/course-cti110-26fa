# CTI 110
# P5LAB1 - Functions
# norris
# 10/20/26

# AFTER: the same walk as p5lab1_before_norris.py, now with functions.
# Each pasted block gets a name with def. Then we call it by name.
# The output is exactly the same as the before file. Check it with diff.

# WHAT THIS TEACHES
#   - def DEFINES a function. Defining it does not run it.
#   - name() CALLS a function. The () is what makes it run.
#   - Write a block once, call it as many times as you like.
#   - Fix a typo in one place and every call gets the fix.
#   - main() as a table of contents: read it to see the whole program.
# Two phases, always: first Python LEARNS the names (the defs),
# then it USES them (the calls). Call a name before its def and Python
# will say it has never heard of you.

# def makes a function. Nothing runs yet. Python just learns the name.
def show_divider():
    # The divider and banner. Written once, used three times.
    # The indented lines below the def line are the function's body.
    print()
    print("=" * 40)
    print("THE FIRST DELVE")
    print("=" * 40)


def show_help():
    # The help block. Written once, used three times.
    print("- Light is time. The torch is a clock you can see.")
    print("- Searching finds things, and it costs a turn.")
    print("- Listen before you open a door. Forcing it makes noise.")


# The three describe_ functions are used once each. A function does not have
# to be repeated to be worth having: a good name is documentation, too.
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
    # name lives only inside main(). The other functions never see it.
    name = input("What is your hero's name? ")
    print(f"Hero: {name}")

    # OUTPUT -- each line is a call: the name, then ()
    # Compare with the BEFORE file: the same three scenes, in the same order,
    # but each scene is now a few short calls instead of pasted blocks.
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
# Without this line the file defines everything and then does nothing.
main()
