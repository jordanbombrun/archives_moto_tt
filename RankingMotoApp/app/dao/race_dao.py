from RankingMotoApp.app.dao.tables_names import Table
from RankingMotoApp.app.database.database_connection import DatabaseConnection
from RankingMotoApp.app.models.race import Format, Race

# les fonctions CREATE retournent l'id de la ligne créee si OK , None si KO 
# les fonctions GET retournent None si KO 

# Race DAO
def create_race(race_p: Race): 
    if race_p.serie is not None:    
        serie_id = get_serie_id(race_p.serie)
        if serie_id is None:
            serie_id = create_serie(race_p.serie)
    race_id = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {Table.race.name} (name, date, location, serie_id) VALUES (?, ?, ?, ?)",
            (race_p.name, race_p.date, race_p.location, serie_id)
        )
        race_id = cursor.lastrowid
    match race_p.format:
        case Format.EXTREME_ENDURO_RACE:
            create_extreme_enduro_race(race_p, race_id)
        case Format.CLASSOC_ENDURO_RACE:
            create_classic_enduro_race(race_p, race_id)
        case Format.CROSS_COUNTRY_RACE:
            create_cross_country_race(race_p, race_id)
        case Format.MOTOCROSS_RACE:
            create_motocross_race(race_p, race_id)
        case Format.ENDURO_SPRINT_RACE:
            create_enduro_sprint_race(race_p, race_id)
    return race_id

# Specific Race DAO
def create_extreme_enduro_race(race_p: Race, race_id: int):
    format_id = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {Table.extreme_enduro_race.name} (race_id, nb_lap, nb_cp) VALUES (?, ?, ?)",
            (race_id, race_p.nb_lap, race_p.nb_cp)
        )
        format_id = cursor.lastrowid
    return format_id

def create_classic_enduro_race(race_p: Race, race_id: int):
    format_id = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {Table.classic_enduro_race.name} (race_id, nb_lap, nb_sp) VALUES (?, ?, ?)",
            (race_id, race_p.nb_lap, race_p.nb_sp)
        )
        format_id = cursor.lastrowid
    return format_id

def create_cross_country_race(race_p: Race, race_id: int):
    format_id = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {Table.cross_country_race.name} (race_id, nb_race) VALUES (?, ?)",
            (race_id, getattr(race_p, 'nb_race', 1))
        )
        format_id = cursor.lastrowid
    return format_id

def create_motocross_race(race_p: Race, race_id: int):
    format_id = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {Table.motocross_race.name} (race_id, nb_race) VALUES (?, ?)",
            (race_id, getattr(race_p, 'nb_race', 1))
        )
        format_id = cursor.lastrowid
    return format_id

def create_enduro_sprint_race(race_p: Race, race_id: int):
    format_id = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {Table.enduro_sprint_race.name} (race_id, nb_lap, nb_sp) VALUES (?, ?, ?)",
            (race_id, race_p.nb_lap, race_p.nb_sp)
        )
        format_id = cursor.lastrowid
    return format_id

# def get_format_id(format_p):
#     format_id = None
#     with DatabaseConnection.get_db_cursor() as cursor:
#         cursor.execute("SELECT id FROM format WHERE name = ?", (format_p.value,))
#         format_line = cursor.fetchone()
#         if format_line:
#             format_id = format_line[0]
#     return format_id

# Race.Serie DAO
def get_serie_id(serie_p):
    serie_id = None
    if serie_p:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(f"SELECT id FROM {Table.serie.name} WHERE name = ? AND year = ?", (serie_p.name, serie_p.year))
            serie_line = cursor.fetchone()
        if serie_line:
            serie_id = serie_line[0]
        # if not serie_id:
        #     serie_id = create_serie(serie_p)
        # else:
        #     serie_id = serie_id[0]
    return serie_id

def create_serie(serie_p):
    serie_id = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(f"INSERT INTO {Table.serie.name} (name, year) VALUES (?, ?)", (serie_p.name, serie_p.year))
        serie_id = cursor.lastrowid
    return serie_id

