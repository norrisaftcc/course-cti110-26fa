# Your Name
# Date
# P5T: The Potion Pouch
# Brief description of program

# This is the potion ritual from The Changekeeper (Potions tab).
# It is the same // and % pattern as your P3LAB, with two potions:
#   Large Potion heals 25 HP. Small Potion heals 5 HP.
# Run it now (it works). In P5T you turn it into a function.

hp_missing = int(input("Enter HP missing: "))

large = hp_missing // 25
hp_missing = hp_missing % 25
if large == 1:
    print(large, "Large Potion")
elif large > 1:
    print(large, "Large Potions")

small = hp_missing // 5
hp_missing = hp_missing % 5
if small == 1:
    print(small, "Small Potion")
elif small > 1:
    print(small, "Small Potions")

print("Still missing:", hp_missing, "HP")
