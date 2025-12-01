# rider.py

from datetime import time

class Rider:
    def __init__(self, name: str = "inconnu", db_id: int = None):
        self.db_id = db_id
        self.name = name

