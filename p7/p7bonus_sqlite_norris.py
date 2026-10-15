# CTI 110
# P7BONUS - SQLite
# norris
# 11/17/26

# A JSON file holds one thing: a story, or a save.
# A DATABASE holds rows in a table, and answers questions about them.
# sqlite3 comes with Python. The whole database is one file: endings.db.
# Here we keep a table of the endings a player has found.

import sqlite3


# Open (or make) the database file and make sure the table exists.
# UNIQUE(story, ending) means the same row can never be stored twice.
def open_db(path):
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS endings ("
        "story TEXT, ending TEXT, UNIQUE(story, ending))"
    )
    return conn


# Store one ending. INSERT OR IGNORE skips a row that is already there.
# The ? marks are filled in by sqlite3, in order. Never paste text into SQL.
def add_ending(conn, story, ending):
    conn.execute("INSERT OR IGNORE INTO endings VALUES (?, ?)", (story, ending))
    conn.commit()     # commit saves the change to the file


# Ask the database how many endings this story has stored
def count_endings(conn, story):
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
    found = count_endings(conn, "fort")
    print(f"Endings found: {found} of {len(all_endings)}")
    conn.close()


# at the bottom -- start the program
main()
