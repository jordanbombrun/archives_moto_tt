import sqlite3
from RankingMotoApp.app.dao.tables_names import Table
from RankingMotoApp.app.database.database_connection import DatabaseConnection
from RankingMotoApp.app.models.rider import Rider
from RankingMotoApp.app.utils.DBReport import DBReport

def dao_create_rider(rider_p: Rider):
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {Table.rider.name} (name) VALUES (?)", 
                (rider_p.name,)
            )
            rider_id = cursor.lastrowid
            rider_p.db_id = rider_id
            return True
    except sqlite3.IntegrityError:
        return DBReport.CREATE_ALREADY_EXISTS
    except Exception:
        return DBReport.CREATE_ERROR
    return False

def dao_get_rider_by_id(rider_id: int):
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM {Table.rider.name} WHERE id = ?",
                (rider_id,)
            )
            row = cursor.fetchone()
            if row:
                return Rider(name=row[1], db_id=row[0])
        return DBReport.GET_NOT_FOUND
    except Exception:
        return DBReport.GET_ERROR

def dao_get_all_riders():
    riders = []
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(f"SELECT * FROM {Table.rider.name}")
            rows = cursor.fetchall()
            for row in rows:
                riders.append(Rider(name=row[1], db_id=row[0]))
        if len(riders) > 0:
            return riders
        return DBReport.GET_NOT_FOUND
    except Exception:
        return DBReport.GET_ERROR