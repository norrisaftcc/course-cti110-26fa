# CTI 110
# P2HW1 - Setup Only
# Talk about how to format the display

# Sample data - real program uses input()
destination = "Raleigh"
budget      = 2000
expenses    = 1000
remaining   = budget - expenses

print(f"{"Destination:":<15} {destination:<15}")
print(f"{"Budget:":<15} ${budget:<15.2f}")
print(f"{"Expenses:":<15} ${expenses:<15.2f}")
print(f"{"Remaining:":<15} ${remaining:<15.2f}")
