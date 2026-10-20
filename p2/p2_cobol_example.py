# Production Pattern: COBOL-Grade Fixed Column Table in Modern Python
# Clean vertical stack, right-aligned decimals, deterministic slot widths

# WHAT THIS TEACHES
#   - Report columns that line up, using f-string width and alignment:
#         {value:<W}  left-align in W spaces
#         {value:>W}  right-align in W spaces
#         {value:>W.2f}  right-align a float with 2 decimals
#   - Put each width in a named constant, so you change it in one place.
#   - A for loop that unpacks each tuple into named parts.
#   - Slicing ([:N]) to cut off text that is too long.
# COBOL programmers did this in the 1960s with PIC clauses, and some of
# those programs still pay your bank. Respect the elders.

# Each employee is a tuple: (name, role, score). A list holds all four.
employees = [
    ("Alice Smith", "Engineer", 94.50),
    ("Bob", "Manager", 100.00),
    ("Maximilian Vance", "Intern", 78.25),
    ("Ada Lovelace", "Lead Arch", 99.80),
]

# 1. Define unambiguous column widths (Spiritual successor to COBOL PIC clauses)
NAME_W  = 18   # PIC X(18)
ROLE_W  = 14   # PIC X(14)
SCORE_W =  8   # PIC ZZ9.99

# 2. Print Header Row with matching alignments
# A width can itself be a variable: {x:<{NAME_W}} reads NAME_W and uses it.
# The header's labels are strings, so we quote them inside the f-string.
header = f"{'EMPLOYEE NAME':<{NAME_W}} {'DEPARTMENT':<{ROLE_W}} {'SCORE':>{SCORE_W}}"
print(header)
# The rule is as long as the header, so it fits even if the widths change.
print("=" * len(header))

# 3. Print Data Rows
# Each pass of the loop splits one tuple into name, role and score.
for name, role, score in employees:
    # Slicing [:NAME_W] prevents long words from breaking column fences
    # (a short name is unchanged; only a name over 18 characters is cut)
    safe_name = name[:NAME_W]
    # Same widths and alignments as the header, so every column lines up.
    print(f"{safe_name:<{NAME_W}} {role:<{ROLE_W}} {score:>{SCORE_W}.2f}")
