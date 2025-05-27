import sqlite3
from flask import make_response, render_template

def get_db_connection():
    conn = sqlite3.connect('/home/jordan/dev/ranking_tracker/archivesmotott.db')
    conn.row_factory = sqlite3.Row
    return conn

def tests():
    conn = get_db_connection()
    c = conn.cursor()
    # posts = conn.execute('SELECT * FROM posts').fetchall()
    c.execute('SELECT * FROM posts')
    rows = c.fetchall()
    for row in rows:
        print(row["title"])
        print(row["content"])
    c.close()
    # strp = ''
    # for p in posts:
    #     strp += p.title
    return make_response('OK')