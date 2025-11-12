import sqlite3
from RankingMotoApp.app.dao.tables_names import Table
from RankingMotoApp.app.database.database_connection import DatabaseConnection
from RankingMotoApp.app.models.participation import Participation
from RankingMotoApp.app.dao.rider_dao import dao_get_rider_by_id
from RankingMotoApp.app.utils.DBReport import DBReport

def dao_create_participation(participation_p: Participation):
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO {Table.participation.name} 
                (race_id, rider_id, number, category_id, final_position, moto) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    participation_p.race.db_id if participation_p.race else None,
                    participation_p.rider.db_id if participation_p.rider else None,
                    participation_p.number,
                    participation_p.category.db_id if participation_p.category else None,
                    participation_p.final_position,
                    None
                )
            )
            participation_p.db_id = cursor.lastrowid
            return True
    except sqlite3.IntegrityError:
        return DBReport.CREATE_ALREADY_EXISTS
    except Exception:
        return DBReport.CREATE_ERROR
    return False

def dao_get_participations_by_race(race_id: int):
    participations = []
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM {Table.participation.name} 
                WHERE race_id = ?""", 
                (race_id,)
            )
            rows = cursor.fetchall()
            for row in rows:
                rider = dao_get_rider_by_id(row[2])
                if rider not in [DBReport.GET_ERROR, DBReport.GET_NOT_FOUND]:
                    participation = Participation(
                        db_id=row[0],
                        rider=rider,
                        final_position=row[5],
                        number=row[4],
                        current_lap=row[6]
                    )
                    participations.append(participation)
        if len(participations) > 0:
            return participations
        return DBReport.GET_NOT_FOUND
    except Exception:
        return DBReport.GET_ERROR