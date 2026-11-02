# Your Name
# Date
# P5T: The Potion Pouch
# Brief description of program

# This is the potion ritual from The Changekeeper (Potions tab).
# It is the same // and % pattern as your P3LAB, with two potions:
#   Large Potion heals 25 HP. Small Potion heals 5 HP.
# Run it now (it works). In P5T you turn it into a function.

# WHAT THIS TEACHES
#   - Reading working code before changing it. Run it, predict it, then edit.
#   - The // and % pattern from P3LAB: // counts the whole potions that fit,
#     % keeps what is left for the next, smaller potion.
#   - Spot the repeat. The large-potion block and the small-potion block are
#     the same shape with different numbers. Repeats are what functions are for.
#   - Your job in P5T: move this into a function. The finished version is
#     in p5t_norris.py. Try it yourself first. The potions will wait.

# The only input. int() turns the typed text into a whole number.
hp_missing = int(input("Enter HP missing: "))

# Large potions first: they heal the most, so they go first.
large = hp_missing // 25            # how many whole Large Potions fit
hp_missing = hp_missing % 25        # the HP still missing after those
# One potion is singular, more than one is plural, zero prints nothing.
# (elif is enough here: the two tests can never both be true.)
if large == 1:
    print(large, "Large Potion")
elif large > 1:
    print(large, "Large Potions")

# Same idea, smaller potion, using what the large potions left over.
small = hp_missing // 5
hp_missing = hp_missing % 5
if small == 1:
    print(small, "Small Potion")
elif small > 1:
    print(small, "Small Potions")

# Anything under 5 HP is left over, because no potion is small enough.
print("Still missing:", hp_missing, "HP")
