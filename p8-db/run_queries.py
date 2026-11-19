import sqlite3

# Connect to database
conn = sqlite3.connect("signup_hw.db")
cursor = conn.cursor()

def print_results(title, query):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    if not rows:
        print("(no rows)")

# 1) Show all users
q1 = "SELECT * FROM users"
print_results("1) All users", q1)

# 2) Show first_name, last_name, email
q2 = "SELECT first_name, last_name, email FROM users"
print_results("2) Name + Email", q2)

# 3) Show users from USA
q3 = "SELECT * FROM users WHERE country = 'USA'"
print_results("3) Users from USA", q3)

# 4) Count total users
q4 = "SELECT COUNT(*) AS total_users FROM users"
print_results("4) Total user count", q4)

# 5) Show 3 most recent signups
q5 = "SELECT username, signup_date FROM users ORDER BY signup_date DESC LIMIT 3"
print_results("5) 3 most recent signups", q5)

# Close connection
conn.close()
print("\n✅ Finished running 5 queries.")