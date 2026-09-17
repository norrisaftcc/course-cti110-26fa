# Production Pattern: COBOL-Grade Fixed Column Table in Modern Python
# Clean vertical stack, right-aligned decimals, deterministic slot widths

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
header = f"{'EMPLOYEE NAME':<{NAME_W}} {'DEPARTMENT':<{ROLE_W}} {'SCORE':>{SCORE_W}}"
print(header)
print("=" * len(header))

# 3. Print Data Rows
for name, role, score in employees:
    # Slicing [:NAME_W] prevents long words from breaking column fences
    safe_name = name[:NAME_W]
    print(f"{safe_name:<{NAME_W}} {role:<{ROLE_W}} {score:>{SCORE_W}.2f}")
