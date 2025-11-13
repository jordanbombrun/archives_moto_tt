import sqlite3
from RankingMotoApp.app.dao.tables_names import Table
from RankingMotoApp.app.database.database_connection import DatabaseConnection
from RankingMotoApp.app.models.race import Category, Format, Race, Race_category, Serie
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

def dao_get_race_by_name_and_date(name_p: str, date_p):
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM {Table.race.name} WHERE name = ? AND date = ?",
                (name_p, date_p)
            )
            row = cursor.fetchone()
            if row:
                res_serie_l = dao_get_serie_by_id(row[4]) 
                serie_l = res_serie_l if isinstance(res_serie_l, Serie) else None
                res_format_l = dao_get_format_by_id(row[5])    
                format_l = res_format_l if isinstance(res_format_l, Format) else None            
                return Race(
                    id=row[0],
                    name=row[1],
                    date=row[2],
                    location=row[3],
                    serie=serie_l,
                    format=format_l
                )
        return DBReport.GET_NOT_FOUND
    except Exception as e:
        return DBReport.GET_ERROR

def dao_get_all_races():
    races = []
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute("""
                SELECT r.id, r.name, r.date, r.location, r.serie_id, r.format_id,
                       s.name as serie_name, s.year as serie_year,
                       f.name as format_name
                FROM race r
                LEFT JOIN serie s ON r.serie_id = s.id
                LEFT JOIN format f ON r.format_id = f.id
            """)
            race_rows = cursor.fetchall()
            for row in race_rows:
                race_id, name, date_val, location, serie_id, format_id, serie_name, serie_year, format_name = row
                serie = Serie(name=serie_name, year=serie_year, id=serie_id) if serie_id else None
                format_obj = Format(name=format_name, id=format_id) if format_id else None
                race = Race(name=name, db_id=race_id, date=date_val, format=format_obj, location=location, serie=serie)
                result_get_categories = dao_get_categories_for_race(race_id)
                if result_get_categories not in [DBReport.GET_NOT_FOUND, DBReport.GET_ERROR]:
                    race.race_categories = result_get_categories
                races.append(race)
        if len(races) > 0: 
            return races
        return DBReport.GET_NOT_FOUND
    except Exception as e:
        return DBReport.GET_ERROR
    
def dao_get_all_races_for_serie(serie_id_p: int):
    races = []
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute("""
                SELECT r.id, r.name, r.date, r.location, r.serie_id, r.format_id,
                       s.name as serie_name, s.year as serie_year,
                       f.name as format_name
                FROM race r
                LEFT JOIN serie s ON r.serie_id = s.id
                LEFT JOIN format f ON r.format_id = f.id
                WHERE r.serie_id = ?
            """, (int(serie_id_p),))    
            race_rows = cursor.fetchall()
            for row in race_rows:
                race_id, name, date_val, location, serie_id, format_id, serie_name, serie_year, format_name = row
                serie = Serie(name=serie_name, year=serie_year, id=serie_id) if serie_id else None
                format_obj = Format(name=format_name, id=format_id) if format_id else None
                race = Race(name=name, db_id=race_id, date=date_val, format=format_obj, location=location, serie=serie)
                result_get_categories = dao_get_categories_for_race(race_id)
                if result_get_categories not in [DBReport.GET_NOT_FOUND, DBReport.GET_ERROR]:
                    race.race_categories = result_get_categories
                races.append(race)
        if len(races) > 0: 
            return races
        return DBReport.GET_NOT_FOUND
    except Exception as e:
        return DBReport.GET_ERROR

# Format Race DAO
def dao_get_all_formats():
    formats = []
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(f"SELECT * FROM {Table.format.name}")
            formats_lines = cursor.fetchall()
        for format_line in formats_lines:
            format_temp = Format(format_line[1], format_line[0])
            formats.append(format_temp)
        if len(formats) > 0:
            return formats
        return DBReport.GET_NOT_FOUND
    except Exception as e:
        return DBReport.GET_ERROR

def dao_get_format_id(format_name :str):    
    format_id = None
    try:
        if format_name:
            with DatabaseConnection.get_db_cursor() as cursor:
                cursor.execute(f"SELECT id FROM {Table.format.name} WHERE name = ?", (format_name.value,))
                format_line = cursor.fetchone()
            if format_line:
                format_id = format_line[0]
        return format_id
    except Exception as e:
        return DBReport.GET_ERROR

def dao_get_format_by_id(format_id :int):
    format_temp = None
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(f"SELECT * FROM {Table.format.name} WHERE id = ?", (format_id,))
            format_line = cursor.fetchone()
        if format_line:
            format_temp = Format(format_line[1], format_line[0])
        return format_temp if format_temp else DBReport.GET_NOT_FOUND
    except Exception as e:
        return DBReport.GET_ERROR

# Race.Serie DAO
def dao_get_all_series():
    series = []
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(f"SELECT * FROM {Table.serie.name}")
            series_lines = cursor.fetchall()
        for serie_line in series_lines:
            serie = Serie(serie_line[1], serie_line[2], serie_line[0])
            series.append(serie)
        if len(series) > 0:
            return series
        return DBReport.GET_NOT_FOUND
    except Exception as e:
        return DBReport.GET_ERROR

def dao_get_serie_id(serie_p :Serie):
    serie_id = None
    try:
        if serie_p:
            with DatabaseConnection.get_db_cursor() as cursor:
                cursor.execute(f"SELECT id FROM {Table.serie.name} WHERE name = ? AND year = ?", (serie_p.name, serie_p.year))
                serie_line = cursor.fetchone()
            if serie_line:
                serie_id = serie_line[0]
        return serie_id
    except Exception as e:
        return DBReport.GET_ERROR
    
def dao_get_serie_by_id(serie_id :int):
    serie_temp = None
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(f"SELECT * FROM {Table.serie.name} WHERE id = ?", (serie_id,))
            serie_line = cursor.fetchone()
        if serie_line:
            serie_temp = Serie(serie_line[1], serie_line[2], serie_line[0])
        return serie_temp if serie_temp else DBReport.GET_NOT_FOUND
    except Exception as e:
        return DBReport.GET_ERROR

def dao_get_serie_id_by_name_and_year(name_p :str, year_p :int):
    serie_id = None
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(f"SELECT * FROM {Table.serie.name} WHERE name = ? AND year = ?", (name_p, year_p))
            serie_line = cursor.fetchone()
        if serie_line:
            serie_id = serie_line[0]
        return serie_id
    except Exception as e:
        return DBReport.GET_ERROR

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

# categories DAO
def dao_get_all_categories():
    categories = []
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(f"SELECT * FROM {Table.category.name}")
            categories_lines = cursor.fetchall()
        for category_line in categories_lines:
            category = Category(category_line[1], category_line[0])
            categories.append(category)
        if len(categories) > 0:
            return categories
        return DBReport.GET_NOT_FOUND
    except Exception as e:
        return DBReport.GET_ERROR

def dao_get_categories_by_ids(categories_ids_p: list[int]):
    categories = []
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            sql_req = f"SELECT * FROM {Table.category.name} WHERE id IN ({','.join(['?'] * len(categories_ids_p))})"
            cursor.execute(sql_req, categories_ids_p)
            categories_lines = cursor.fetchall()
        for category_line in categories_lines:
            category = Category(category_line[1], category_line[0])
            categories.append(category)
        if len(categories) > 0:
            return categories
        return DBReport.GET_NOT_FOUND
    except Exception as e:
        return DBReport.GET_ERROR

def dao_get_race_categories_by_id(categories_ids_p: list[int]):
    race_categories = []
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            sql_req = f"SELECT * FROM {Table.race_category.name} WHERE category_id IN ({','.join(['?'] * len(categories_ids_p))})"
            cursor.execute(sql_req, categories_ids_p)
            race_categories_lines = cursor.fetchall()
        for race_category_line in race_categories_lines:
            race_categories = Race_category(race_category_line[0], race_category_line[1], race_category_line[2], race_category_line[3], race_category_line[4], race_category_line[5])
        if len(race_categories) > 0:
            return  race_categories
        return DBReport.GET_NOT_FOUND
    except Exception as e:
        return DBReport.GET_ERROR
    
def dao_get_category_by_id(category_id_p: int):
    category = None
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(f"SELECT * FROM {Table.category.name} WHERE id = ?", (category_id_p,))
            category_line = cursor.fetchone()
        if category_line:
            category = Category(category_line[1], category_line[0])
        return category if category else DBReport.GET_NOT_FOUND
    except Exception as e:
        return DBReport.GET_ERROR
    
def dao_get_categories_for_race(race_id_p: int):
    categories = []
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute("""
                SELECT c.id, c.name
                FROM race_category rc
                JOIN category c ON rc.category_id = c.id
                WHERE   rc.race_id = ?
            """, (race_id_p,))
            categories_lines = cursor.fetchall()
        for category_line in categories_lines:
            category = Category(category_line[1], category_line[0])
            categories.append(category)
        if len(categories) > 0:
            return categories
        return DBReport.GET_NOT_FOUND
    except Exception as e:
        return DBReport.GET_ERROR   

def dao_create_race_category(race_category_p: Race_category):
    try:
        with DatabaseConnection.get_db_cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {Table.race_category.name} (race_id, category_id, nb_lap, nb_cp, nb_sp, nb_round) VALUES (?, ?, ?, ?, ?, ?)",
                (race_category_p.db_race_id, race_category_p.category_id, 0, 0, 0, 0)
            )
    except sqlite3.IntegrityError as e:
        return DBReport.CREATE_ALREADY_EXISTS
    except Exception as e:
        return DBReport.CREATE_ERROR
    return True

#     CREATE TABLE IF NOT EXISTS "race_category" (
# 	"race_id" INTEGER NOT NULL UNIQUE,
# 	"category_id" INTEGER NOT NULL,
# 	"nb_lap" INTEGER,
# 	"nb_cp" INTEGER,
# 	"nb_sp" INTEGER,
# 	"nb_round" INTEGER,
# 	PRIMARY KEY("race_id", "category_id"),
# 	FOREIGN KEY ("race_id") REFERENCES "race"("id")
# 	ON UPDATE CASCADE ON DELETE CASCADE,
# 	FOREIGN KEY ("category_id") REFERENCES "category"("id")
# 	ON UPDATE CASCADE ON DELETE CASCADE
# );