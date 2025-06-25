from contextlib import contextmanager
import sqlite3
import os

class DatabaseConnection:
    _db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivesmotott.db')

    @staticmethod
    @contextmanager
    def get_db_cursor():
        conn = sqlite3.connect(DatabaseConnection._db_path)
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            conn.close()

