import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'archivesmotott.db')
schema_path = os.path.join(current_dir, 'schema.sql')

try:
    connection = sqlite3.connect(db_path)

    with open(schema_path, 'r') as f:
        connection.executescript(f.read())

    print("BDD OK")

    # cur = connection.cursor()

    # Uncomment below to insert sample data into the 'posts' table
    # cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
    #             ('First Post', 'Content for the first post')
    #             )
    # cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
    #             ('Second Post', 'Content for the second post')
    #             )


except Exception as e:
    print("BDD KO") 
    print(f"Erreur : {e}")
finally:
    connection.commit()
    connection.close()