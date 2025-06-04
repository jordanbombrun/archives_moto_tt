import sqlite3
import os

class DatabaseConnection:
    _db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivesmotott.db')
    _connection = None

    @staticmethod
    def connect():
        if DatabaseConnection._connection is None:
            DatabaseConnection._connection = sqlite3.connect(DatabaseConnection._db_path)
        return DatabaseConnection._connection

    @staticmethod
    def close():
        if DatabaseConnection._connection:
            DatabaseConnection._connection.close()
            DatabaseConnection._connection = None
