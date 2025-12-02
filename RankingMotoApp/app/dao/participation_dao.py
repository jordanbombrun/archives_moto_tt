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
                # res_cat = dao_get_category_by_id(row[4])  # category_id est maintenant à l'index 4
                # category_l = res_cat if isinstance(res_cat, Category) else None
                participation = Participation(
                    db_id=row[0],  # id
                    rider=rider_p,
                    final_position=row[6],  # final_position est maintenant à l'index 6 (après id, race_id, rider_id, number, category_id, team_id)
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
                rider = dao_get_rider_by_id(row[2])  # rider_id est maintenant à l'index 2 (après id, race_id)
                if rider not in [DBReport.GET_ERROR, DBReport.GET_NOT_FOUND]:
                    participation = Participation(
                        db_id=row[0],  # id
                        rider=rider,
                        final_position=row[6],  # final_position est maintenant à l'index 6
                        number=row[3]  # number est maintenant à l'index 3
                    )
                    participations.append(participation)
                else: 
                    return DBReport.GET_ERROR
        if len(participations) > 0:
            return participations
        return DBReport.GET_NOT_FOUND
    except Exception:
        return DBReport.GET_ERROR

# Chrono DAO
def dao_create_chrono(participation: Participation, current_lap: int = None, current_pt: int = None, time: float = 0.0):
    try:
        if not participation or not participation.db_id:
            return DBReport.CREATE_ERROR
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO {Table.chrono.name} 
                (participation_id, current_lap, current_pt, time) 
                VALUES (?, ?, ?, ?)""",
                (
                    participation.db_id,
                    current_lap,
                    current_pt,
                    time
                )
            )
            return True
    except sqlite3.IntegrityError:
        return DBReport.CREATE_ALREADY_EXISTS
    except Exception:
        return DBReport.CREATE_ERROR
    return False

def dao_create_participation_chronos(participation: Participation):
    try:
        if not participation or not hasattr(participation, "chronos_lap_CP"):
            return DBReport.CREATE_ERROR
        for lap_index, chrono_list in enumerate(participation.chronos_lap_CP):
            current_lap = lap_index + 1  # 1-based lap
            for pt_index, chrono in enumerate(chrono_list):
                current_pt = pt_index + 1  # 1-based pt (point spécial, CP, etc.)
                # Convertir le time object en float (minutes)
                if isinstance(chrono, float):
                    time_value = chrono
                elif hasattr(chrono, "hour") and hasattr(chrono, "minute"):
                    time_value = chrono.hour * 60 + chrono.minute + (chrono.second / 60.0 if hasattr(chrono, "second") else 0.0)
                else:
                    time_value = 0.0
                
                result = dao_create_chrono(
                    participation=participation,
                    current_lap=current_lap,
                    current_pt=current_pt,
                    time=time_value
                )
                if result in (DBReport.CREATE_ERROR, False):
                    return DBReport.CREATE_ERROR
        return True
    except Exception:
        return DBReport.CREATE_ERROR

def dao_get_chrono_by_id(chrono_id: int):
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM {Table.chrono.name} 
                WHERE id = ?""",
                (chrono_id,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'participation_id': row[1],
                    'current_lap': row[2],
                    'current_pt': row[3],
                    'time': row[4]
                }
        return DBReport.GET_NOT_FOUND
    except Exception:
        return DBReport.GET_ERROR

def dao_get_chronos_by_participation(participation: Participation):
    chronos = []
    try:
        if not participation or not participation.db_id:
            return DBReport.GET_ERROR
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM {Table.chrono.name} 
                WHERE participation_id = ?""",
                (participation.db_id,)
            )
            rows = cursor.fetchall()
            for row in rows:
                chronos.append({
                    'id': row[0],
                    'participation_id': row[1],
                    'current_lap': row[2],
                    'current_pt': row[3],
                    'time': row[4]
                })
        if len(chronos) > 0:
            return chronos
        return DBReport.GET_NOT_FOUND
    except Exception:
        return DBReport.GET_ERROR

def dao_update_chrono(chrono_id: int, current_lap: int = None, current_pt: int = None, time: float = None):
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            # Construire la requête UPDATE dynamiquement selon les paramètres fournis
            updates = []
            params = []
            
            if current_lap is not None:
                updates.append("current_lap = ?")
                params.append(current_lap)
            if current_pt is not None:
                updates.append("current_pt = ?")
                params.append(current_pt)
            if time is not None:
                updates.append("time = ?")
                params.append(time)
            
            if not updates:
                return DBReport.UPDATE_ERROR
            
            params.append(chrono_id)
            cursor.execute(
                f"""UPDATE {Table.chrono.name} 
                SET {', '.join(updates)} 
                WHERE id = ?""",
                tuple(params)
            )
            if cursor.rowcount > 0:
                return DBReport.UPDATE_OK
            return DBReport.UPDATE_NOT_FOUND
    except Exception:
        return DBReport.UPDATE_ERROR

def dao_delete_chrono(chrono_id: int):
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(
                f"""DELETE FROM {Table.chrono.name} 
                WHERE id = ?""",
                (chrono_id,)
            )
            if cursor.rowcount > 0:
                return DBReport.DELETE_OK
            return DBReport.DELETE_NOT_FOUND
    except Exception:
        return DBReport.DELETE_ERROR

def dao_delete_chronos_by_participation(participation: Participation):
    try:
        if not participation or not participation.db_id:
            return DBReport.DELETE_ERROR
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(
                f"""DELETE FROM {Table.chrono.name} 
                WHERE participation_id = ?""",
                (participation.db_id,)
            )
            return DBReport.DELETE_OK
    except Exception:
        return DBReport.DELETE_ERROR