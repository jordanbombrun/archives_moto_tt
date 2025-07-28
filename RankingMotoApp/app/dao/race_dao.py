import sqlite3
from RankingMotoApp.app.dao.tables_names import Table
from RankingMotoApp.app.database.database_connection import DatabaseConnection
from RankingMotoApp.app.models.race import Format, Race, Serie
from RankingMotoApp.app.utils.DBReport import DBReport

# les fonctions CREATE retournent l'id de la ligne créee si OK , None si KO 
# les fonctions GET retournent None si KO 

# Race DAO
# Serie and Format are not created here
# return True if OK
def dao_create_race(race_p: Race):      
    race_id = None
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {Table.race.name} (name, date, location, serie_id, format_id) VALUES (?, ?, ?, ?, ?)",
                (race_p.name, race_p.date, race_p.location, race_p.serie.db_id, race_p.format.db_id)
            )
            race_id = cursor.lastrowid
            if race_id is not None:
                race_p.db_id = race_id
                return True
    except sqlite3.IntegrityError:
        return DBReport.CREATE_ALREADY_EXISTS
    except Exception:
        return DBReport.CREATE_ERROR
    return False

# Format Race DAO
def dao_get_all_formats():
    formats = []
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(f"SELECT * FROM {Table.format.name}")
        formats_lines = cursor.fetchall()
    for format_line in formats_lines:
        format_temp = Format(format_line[1], format_line[0])
        formats.append(format_temp)
    if len(formats) > 0:
        return formats
    return DBReport.GET_NOT_FOUND

def dao_get_format_id(format_name :str):    
    format_id = None
    if format_name:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(f"SELECT id FROM {Table.format.name} WHERE name = ?", (format_name.value,))
            format_line = cursor.fetchone()
        if format_line:
            format_id = format_line[0]
            return format_id
    return DBReport.GET_NOT_FOUND

def dao_get_format_by_id(format_id :int):
    format_temp = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(f"SELECT * FROM {Table.format.name} WHERE id = ?", (format_id,))
        format_line = cursor.fetchone()
    if format_line:
        format_temp = Format(format_line[1], format_line[0])
    return format_temp if format_temp else DBReport.GET_NOT_FOUND

# Race.Serie DAO
def dao_get_all_series():
    series = []
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(f"SELECT * FROM {Table.serie.name}")
        series_lines = cursor.fetchall()
    for serie_line in series_lines:
        serie = Serie(serie_line[1], serie_line[2], serie_line[0])
        series.append(serie)
    if len(series) > 0:
        return series
    return DBReport.GET_NOT_FOUND

def dao_get_serie_id(serie_p :Serie):
    serie_id = None
    if serie_p:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(f"SELECT id FROM {Table.serie.name} WHERE name = ? AND year = ?", (serie_p.name, serie_p.year))
            serie_line = cursor.fetchone()
        if serie_line:
            serie_id = serie_line[0]
    return serie_id

def dao_get_serie_by_id(serie_id :int):
    serie_temp = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(f"SELECT * FROM {Table.serie.name} WHERE id = ?", (serie_id,))
        serie_line = cursor.fetchone()
    if serie_line:
        serie_temp = Serie(serie_line[1], serie_line[2], serie_line[0])
    return serie_temp if serie_temp else DBReport.GET_NOT_FOUND

def dao_get_serie_id_by_name_and_year(name_p :str, year_p :int):
    serie_id = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(f"SELECT * FROM {Table.serie.name} WHERE name = ? AND year = ?", (name_p, year_p))
        serie_line = cursor.fetchone()
    if serie_line:
        serie_id = serie_line[0]
    return serie_id

def dao_create_serie(serie_p :Serie):
    serie_id = None
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(f"INSERT INTO {Table.serie.name} (name, year) VALUES (?, ?)", (serie_p.name, serie_p.year))
            serie_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        return DBReport.CREATE_ALREADY_EXISTS
    except Exception:
        return DBReport.CREATE_ERROR
    return serie_id

