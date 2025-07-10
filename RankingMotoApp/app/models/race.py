from datetime import date

class Format:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

class Serie:
    def __init__(self, id: int, name: str, year: int):
        self.id = id
        self.name = name
        self.year = year

class Race:
    def __init__(self, name: str, date: date = date(2000, 1, 1), format: Format = None, location: str = 'inconnu', serie: Serie = None, nb_CP: int = 0, nb_SP: int = 0, nb_laps: int = 0, nb_rounds: int = 0):
        self.name = name
        self.date = date
        self.format = format if isinstance(format, Format) else None
        self.serie = serie if isinstance(serie, Serie) else None
        self.location = location
        self.riders = []
        self.nb_cp = nb_CP
        self.nb_sp = nb_SP
        self.nb_lap = nb_laps
        self.nb_round = nb_rounds


    def add_riders(self, riders_P):
        self.riders.extend(riders_P)  # Ajoute tous les pilotes à la liste

    def get_rider_by_number(self, number_P):
        for p in self.riders:
            if (p.number == number_P):
                return p
        return None

    def get_race(self):
        return 'classement de la course ' + self.name + ' ' + str(self.date.year)

