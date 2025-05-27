import os
import sqlite3

# current_dir = os.getcwd()

connection = sqlite3.connect('archivesmotott.db')


with open('RankingMotoApp/app/database/test.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

connection.commit()
connection.close()