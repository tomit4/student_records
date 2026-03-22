import sqlite3

con = sqlite3.connect("tutorial.db")
cur = con.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS movies(
                movie_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year TEXT NOT NULL,
                score REAL)
            """)

movies = [
    ("Monty Python and the Holy Grail", 1975, 8.2),
    ("And Now for Something Completely Different", 1971, 7.5),
]

cur.executemany("INSERT INTO movies(title, year, score) VALUES (?, ?, ?)", movies)

con.commit()

res = cur.execute("SELECT * FROM movies")
print("res.fetchall() :=> ", res.fetchall())
