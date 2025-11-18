from datetime import date

class Format:
    def __init__(self, name: str, id: int = None):
        self.db_id = id
        self.name = name

class Serie:
    def __init__(self, name: str, year: int, id: int = None):
        self.db_id = id
        self.name = name
        self.year = year

class Category:
    def __init__(self, name: str, id: int = None):
        self.db_id = id
        self.name = name

class Race_category:
    def __init__(self, race_id: int, category_id: int):
        self.db_race_id = race_id
        self.category_id = category_id

    @property
    def nb_lap(self):
        return self._nb_lap

    @nb_lap.setter
    def nb_lap(self, value: int):
        self._nb_lap = value

    @property
    def nb_cp(self):
        return self._nb_cp

    @nb_cp.setter
    def nb_cp(self, value: int):
        self._nb_cp = value

    @property
    def nb_sp(self):
        return self._nb_sp

    @nb_sp.setter
    def nb_sp(self, value: int):
        self._nb_sp = value

    @property
    def nb_round(self):
        return self._nb_round

    @nb_round.setter
    def nb_round(self, value: int):
        self._nb_round = value


class Race:
    def __init__(self, name: str, 
                 db_id: int = None, 
                 date: date = date(2000, 1, 1), 
                 format: Format = None, 
                 location: str = 'inconnu', 
                 serie: Serie = None, 
                 race_categories: list[Race_category] = None):
        self.db_id = db_id
        self.name = name
        self.date = date
        self.format = format if isinstance(format, Format) else None
        self.serie = serie if isinstance(serie, Serie) else None
        self.location = location
        self.participations = [] 
        if isinstance(race_categories, list) and all(isinstance(cat, Race_category) for cat in race_categories):
            self.race_categories = race_categories
        else:
            self.race_categories = None

    # def __init__(self, name: str, 
    #              db_id: int= 0, 
    #              date: date = date(2000, 1, 1), 
    #              format: Format = None, 
    #              location: str = 'inconnu', 
    #              serie: Serie = None):
    #     self._db_id = db_id
    #     self.name = name
    #     self.date = date
    #     self.location = location
    #     self.serie = serie if isinstance(serie, Serie) else None
    #     self.format = format if isinstance(format, Format) else None

    # def add_riders(self, riders_P):
    #     self.riders.extend(riders_P)  # Ajoute tous les pilotes à la liste

    # def get_rider_by_number(self, number_P):
    #     for p in self.riders:
    #         if (p.number == number_P):
    #             return p
    #     return None

    def get_race(self):
        return 'classement de la course ' + self.name + ' ' + str(self.date.year)
    
    @property
    def db_id(self):
        return self._db_id
    
    @db_id.setter
    def db_id(self, value: int):
        self._db_id = value

    # @property
    # def race_categories(self):
    #     return self._race_categories

    # @race_categories.setter
    # def race_categories(self, value: list[Race_category]):
    #     self._race_categories = value


