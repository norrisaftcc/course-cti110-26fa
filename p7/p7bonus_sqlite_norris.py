# CTI 110
# P7BONUS - SQLite
# norris
# 11/17/26

# A JSON file holds one thing: a story, or a save.
# A DATABASE holds rows in a table, and answers questions about them.
# sqlite3 comes with Python. The whole database is one file: endings.db.
# Here we keep a table of the endings a player has found.

# WHAT THIS TEACHES
#   - A database is a set of TABLES. A table has COLUMNS (story, ending)
#     and ROWS (one per fact). You ask it questions in SQL.
#   - The usual steps: connect, execute, commit (if you changed anything), close.
#   - Constraints: UNIQUE makes the database refuse duplicates for you, so
#     your Python does not need to check.
#   - Parameters (?): how to put values into SQL without pasting text in.
#     Pasted text is how "Little Bobby Tables" drops your school's database.
#     (Search for xkcd 327. It is funny until it is your database.)
# Run it twice. The count stays at 2, because the file remembers.
# That is the difference between a database and a variable.

import sqlite3


# Open (or make) the database file and make sure the table exists.
# UNIQUE(story, ending) means the same row can never be stored twice.
def open_db(path):
    # connect() opens the file, or creates it if it is not there yet.
    conn = sqlite3.connect(path)
    # IF NOT EXISTS makes this safe to run every time: the table is made
    # on the first run and left alone after that.
    conn.execute(
        "CREATE TABLE IF NOT EXISTS endings ("
        "story TEXT, ending TEXT, UNIQUE(story, ending))"
    )
    return conn


# Store one ending. INSERT OR IGNORE skips a row that is already there.
# The ? marks are filled in by sqlite3, in order. Never paste text into SQL.
def add_ending(conn, story, ending):
    # The tuple (story, ending) fills the two ? marks, first to first.
    conn.execute("INSERT OR IGNORE INTO endings VALUES (?, ?)", (story, ending))
    conn.commit()     # commit saves the change to the file


# Ask the database how many endings this story has stored
def count_endings(conn, story):
    # COUNT(*) is one number: how many rows match. fetchone() returns that
    # one row as a tuple, such as (2,). row[0] is the number inside it.
    row = conn.execute("SELECT COUNT(*) FROM endings WHERE story = ?", (story,)).fetchone()
    return row[0]


def main():
    # The Fort story has three endings
    all_endings = ["flooded_stair", "rowed_home", "fell"]

    # PROCESSING -- pretend the player reached these endings, in this order.
    # flooded_stair twice: the table keeps it only once.
    conn = open_db("endings.db")
    add_ending(conn, "fort", "flooded_stair")
    add_ending(conn, "fort", "rowed_home")
    add_ending(conn, "fort", "flooded_stair")

    # OUTPUT
    # Three inserts, but one was a repeat, so this prints 2 of 3.
    found = count_endings(conn, "fort")
    print(f"Endings found: {found} of {len(all_endings)}")
    # Close the connection when finished, like closing a file.
    conn.close()


# at the bottom -- start the program
main()
