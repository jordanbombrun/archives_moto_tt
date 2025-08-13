from enum import Enum

# all table names used in the app
# name : DB table name
# value : text to be used in the app UI
class Table(Enum):
    race = "course"
    serie = "serie"
    team = "team"
    format = "format"
    category = "categorie"
    race_category = "race_category"
    rider = "pilote"
    log_import_data = "log_import_data"
    participation = "participation"
    checkpoint = "checkpoint"
    chrono = "chrono"
    penalty = "penalité"

    # specifics races
    extreme_enduro_race = "enduro extrême"
    cross_country_race = "cross country"
    motocross_race = "motocross"
    classic_enduro_race = "enduro"
    enduro_sprint_race = "enduro sprint"
