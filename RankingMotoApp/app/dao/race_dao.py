from RankingMotoApp.app.database.database_connection import DatabaseConnection
from RankingMotoApp.app.models.race import Race

# les fonctions CREATE retournent l'id de la ligne créee si OK , None si KO 
# les fonctions GET retournent None si KO 

# Race DAO
def save_race(race_p: Race): 
    if race_p.serie is not None:    
        serie_id = get_serie_id(race_p.serie)
        if serie_id is None:
            serie_id = create_serie(race_p.serie)
    format_id = get_format_id(race_p.format)
    race_id = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute(
            "INSERT INTO race (name, date, location, format_id, serie_id) VALUES (?, ?, ?, ?, ?)",
            (race_p.name, race_p.date, race_p.location, format_id, serie_id)
        )
        race_id = cursor.lastrowid
    return race_id

# Race.Format DAO
def get_format_id(format_p):
    format_id = None
    with DatabaseConnection.get_db_cursor() as cursor:
        cursor.execute("SELECT id FROM format WHERE name = ?", (format_p.value,))
        format_line = cursor.fetchone()
        if format_line:
            format_id = format_line[0]
    return format_id

# Race.Serie DAO
def get_serie_id(serie_p):
    serie_id = None
    if serie_p:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute("SELECT id FROM serie WHERE name = ? AND year = ?", (serie_p.name, serie_p.year))
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
        cursor.execute("INSERT INTO serie (name, year) VALUES (?, ?)", (serie_p.name, serie_p.year))
        serie_id = cursor.lastrowid
    return serie_id


# Table race {
# 	id integer [ pk, increment, not null, unique ]
# 	name varchar [ not null ]
# 	date date [ not null ]
# 	location varchar
# 	format_id integer
# 	serie_id integer
# }

# CREATE TABLE IF NOT EXISTS "serie" (
# 	"id" INTEGER NOT NULL UNIQUE,
# 	"name" REAL,
# 	"year" INTEGER,
# 	PRIMARY KEY("id")
# );