# CTI 110
# DHW1
# Norris
# 11/19/26
# My version of DHW1.

import sqlite3

# Connect to SQLite database file (creates file if it doesn't exist)
conn = sqlite3.connect("signup_hw.db")
cursor = conn.cursor()

# Drop table so script can be re-run cleanly in class
cursor.execute("DROP TABLE IF EXISTS users")

# STUDENT CODE GOES IN THIS SECTION ONLY!!!
#--------------------------------------------------------------------------------------
# STEP 1: Create users table
# TO DO: Create a table called users with fields
# user_id, first_name, last_name, email, username, password_hash, signup_date, country, age
# I have started the table for you with the primary key 'user_id'
# NOTE: SQLite assigns user_id for you. You do not insert a value for it.
# NOTE: Do not put a comma after the LAST column in the table. A trailing comma is a syntax error.
cursor.execute("""
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    username TEXT,
    password_hash TEXT,
    signup_date DATE,
    country TEXT,
    age INTEGER
)""")

# STEP 2: Insert sample fake users
# TO DO: Create a list called users that will store all 10 of your fake users information.
# I have started it for you
# Each user has 8 values, in this order (user_id is NOT included):
# first_name, last_name, email, username, password_hash, signup_date, country, age

users = [
    ('Naruto', 'Uzumaki', 'ramen@example.com', 'naruto_u', 'LoveRamen1', '2026-06-01', 'JAPAN', 16),
    ('Monkey D.', 'Luffy', 'meat@example.com', 'luffy_m', 'KingPirate1', '2026-06-02', 'JAPAN', 17),
    ('Goku', 'Son', 'training@example.com', 'goku_s', 'SaiyanPower1', '2026-06-03', 'JAPAN', 18),
    ('Tanjiro', 'Kamado', 'wisteria@example.com', 'tanjiro_k', 'Hinokami1', '2026-06-04', 'JAPAN', 15),
    ('Peter', 'Parker', 'webslinger@example.com', 'peter_p', 'SpideySense1', '2026-06-05', 'USA', 17),
    ('Ichigo', 'Kurosaki', 'soulreaper@example.com', 'ichigo_k', 'BankaiBleach1', '2026-06-06', 'JAPAN', 17),
    ('Edward', 'Elric', 'alchemy@example.com', 'edward_e', 'Fullmetal1', '2026-06-07', 'AMESTRIS', 16),
    ('Spike', 'Spiegel', 'bebop@example.com', 'spike_s', 'SeeYouSpace1', '2026-06-08', 'MARS', 27),
    ('Light', 'Yagami', 'justice@example.com', 'light_y', 'DeathNote1', '2026-06-09', 'JAPAN', 17),
    ('Clark', 'Kent', 'dailyplanet@example.com', 'clark_k', 'KryptonSon1', '2026-06-10', 'USA', 28),
]


#------------------------------------------------------------------------------------
# DO NOT CODE PAST HERE!!!
# STEP 3: Run the python script! Once your done creating your table and adding in the user information
# You should run the program and it will create your database called signup_hw.db.
# You can then view it in your terminal and you can upload the .db file to a database viewer thats provided on Canvas.

cursor.executemany("""
INSERT INTO users (
    first_name, last_name, email, username, password_hash,
    signup_date, country, age
) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", users)

conn.commit()
conn.close()

print("✅ signup_hw.db created with users table and sample data.")

print()

conn = sqlite3.connect("signup_hw.db")
cur = conn.cursor()
for row in cur.execute("SELECT * FROM users LIMIT 10"):
    print(row)
conn.close()