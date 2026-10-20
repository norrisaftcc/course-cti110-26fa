# CTI 110
# P5LAB1 - Functions
# norris
# 10/20/26

# BEFORE: a short walk on the Isle of Old Stone, written top to bottom.
# It works. But look for blocks that are pasted more than once.
# The fixed version, p5lab1_norris.py, prints exactly the same output.

# WHAT THIS TEACHES
#   - The problem functions solve: the same lines pasted again and again.
#   - Copy and paste works. It also writes a bug in three places at once.
#     Change the banner text and you must find and fix every copy.
#   - Read this file first. Count the repeats. Then open the AFTER file.
# Programmers call the cure DRY: Don't Repeat Yourself. The cure for the
# disease of repeating yourself is, ironically, to say it once.

# INPUT
name = input("What is your hero's name? ")
print(f"Hero: {name}")

# The divider and banner
# (This block appears again below. P5LAB1 fixes that.)
# Copy 1 of 3 of the banner.
print()
print("=" * 40)
print("THE FIRST DELVE")
print("=" * 40)

# The docks
print("The Fort docks. Captain Maren coils a wet rope and does not smile.")
print("\"Row to the Isle of Old Stone. Find out who lands there,")
print("and what moves in the water.\"")

# The help block
# (This block appears again below. P5LAB1 fixes that.)
# Copy 1 of 3 of the help text.
print("- Light is time. The torch is a clock you can see.")
print("- Searching finds things, and it costs a turn.")
print("- Listen before you open a door. Forcing it makes noise.")

# (This block appears again below. P5LAB1 fixes that.)
# Copy 2 of 3 of the banner.
print()
print("=" * 40)
print("THE FIRST DELVE")
print("=" * 40)

# The jetty
print("S1. THE BROKEN JETTY")
print("A stone jetty runs out from the south shore. Half of it has fallen")
print("into the lake. On a mooring post, a rope burn shows pale and fresh:")
print("someone else lands here.")

# (This block appears again below. P5LAB1 fixes that.)
# Copy 2 of 3 of the help text.
print("- Light is time. The torch is a clock you can see.")
print("- Searching finds things, and it costs a turn.")
print("- Listen before you open a door. Forcing it makes noise.")

# (This block appeared twice above. P5LAB1 fixes that.)
# Copy 3 of 3 of the banner.
print()
print("=" * 40)
print("THE FIRST DELVE")
print("=" * 40)

# The tower shell
print("S2. THE TOWER SHELL")
print("A round tower, thirty feet across, open to the sky. Its upper floors")
print("fell in long ago and lie as rubble on the ground.")

# (This block appeared twice above. P5LAB1 fixes that.)
# Copy 3 of 3 of the help text.
print("- Light is time. The torch is a clock you can see.")
print("- Searching finds things, and it costs a turn.")
print("- Listen before you open a door. Forcing it makes noise.")
