import sqlite3
from RankingMotoApp.app.dao.race_dao import *
from RankingMotoApp.app.dao.tables_names import Table
from RankingMotoApp.app.database.database_connection import DatabaseConnection
from RankingMotoApp.app.models.participation import Participation
from RankingMotoApp.app.dao.rider_dao import *
from RankingMotoApp.app.models.race import Category, Race
from RankingMotoApp.app.models.rider import Rider
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

def dao_get_participation_by_race_rider(race_p: Race, rider_p: Rider):
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM {Table.participation.name} 
                WHERE race_id = ? AND rider_id = ?""",  
                (race_p.db_id, rider_p.db_id)
            )
            row = cursor.fetchone()
            if row:
                # res_cat = dao_get_category_by_id(row[3])
                # category_l = res_cat if isinstance(res_cat, Category) else None
                participation = Participation(
                    db_id=row[0],
                    rider=rider_p,
                    final_position=row[5],
                    race=race_p
                )
                return participation
        return DBReport.GET_NOT_FOUND
    except Exception as e:
        return DBReport.GET_ERROR

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
                rider = dao_get_rider_by_id(row[1])
                if rider not in [DBReport.GET_ERROR, DBReport.GET_NOT_FOUND]:
                    participation = Participation(
                        db_id=row[0],
                        rider=rider,
                        final_position=row[5],
                        number=row[2]
                    )
                    participations.append(participation)
                else: 
                    return DBReport.GET_ERROR
        if len(participations) > 0:
            return participations
        return DBReport.GET_NOT_FOUND
    except Exception:
        return DBReport.GET_ERROR