from datetime import date
from enum import Enum

# Format name in the app, it has to match the DB tables names
class Format(Enum):
    CASSIC_ENDURO_RACE = "enduro classique"
    ENDURO_SPRINT_RACE = "enduro sprint"
    EXTREME_ENDURO_RACE = "enduro extrême"
    CROSS_COUNTRY_RACE = "cross country"
    MOTOCROSS_RACE = "motocross"
    INCONNU = "inconnu"

class Serie:
    def __init__(self, name: str, year: int):
        self.name = name
        self.year = year

class Race:
    def __init__(self, name: str, date: date = date(2000, 1, 1), format: Format = Format.INCONNU, location: str = 'inconnu', serie: Serie = None, nb_CP: int = 0, nb_SP: int = 0, nb_laps: int = 0):
        self.name = name
        self.date = date
        # Convert string format to Format enum
        if isinstance(format, Format):
            self.format = format
        else:
            self.format = Format(format) if format in Format._value2member_map_ else Format.INCONNU
        self.serie = serie if isinstance(serie, Serie) else None
        self.location = location
        self.riders = []
        self.nb_cp = nb_CP
        self.nb_sp = nb_SP
        self.nb_lap = nb_laps

    def add_riders(self, riders_P):
        self.riders.extend(riders_P)  # Ajoute tous les pilotes à la liste

    def get_rider_by_number(self, number_P):
        for p in self.riders:
            if (p.number == number_P):
                return p
        return None

    def get_race(self):
        return 'classement de la course ' + self.name + ' ' + str(self.date.year)

