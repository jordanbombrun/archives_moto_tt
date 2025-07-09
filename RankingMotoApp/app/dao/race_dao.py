from RankingMotoApp.app.dao.tables_names import Table
from RankingMotoApp.app.database.database_connection import DatabaseConnection
from RankingMotoApp.app.models.race import Format, Race, Serie

# les fonctions CREATE retournent l'id de la ligne créee si OK , None si KO 
# les fonctions GET retournent None si KO 

# Race DAO
# Serie is created if not exists
# Format is not created, only retrieved
def create_race(race_p: Race): 
    # serie
    if race_p.serie is not None:    
        serie_id = get_serie_id(race_p.serie)
        if serie_id is None:
            serie_id = create_serie(race_p.serie)
    # race format        
    format_id = None
    if race_p.format is not None:
        format_id = get_format_id(race_p.format)
    
    # race        
    race_id = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {Table.race.name} (name, date, location, serie_id, format_id) VALUES (?, ?, ?, ?, ?)",
            (race_p.name, race_p.date, race_p.location, serie_id, format_id)
        )
        race_id = cursor.lastrowid
    return race_id

# Format Race DAO
def get_format_id(format_p :Format):    
    format_id = None
    if format_p:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute("SELECT id FROM format WHERE name = ?", (format_p.value,))
            format_line = cursor.fetchone()
        if format_line:
            format_id = format_line[0]
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
def get_serie_id(serie_p :Serie):
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

def create_serie(serie_p :Serie):
    serie_id = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(f"INSERT INTO {Table.serie.name} (name, year) VALUES (?, ?)", (serie_p.name, serie_p.year))
        serie_id = cursor.lastrowid
    return serie_id

