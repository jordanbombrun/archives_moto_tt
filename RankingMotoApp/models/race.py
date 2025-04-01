# course.py

from datetime import date

class Race:
    def __init__(self, name, date = date(2000, 1, 1), type = "inconnu", nb_CP = 0, nb_laps = 0) :
        self.name = name
        self.date = date
        self.type = type # enum : enduro classique, endurance cross, course à CP
        self.riders = [] # liste des pilotes
        self.nb_CP = nb_CP # nb CP par tour
        self.nb_laps = nb_laps # nb tours

    def add_riders(self, riders_P):
        self.riders.extend(riders_P)  # Ajoute tous les pilotes à la liste

    def get_rider_by_number(self, number_P):
        for p in self.riders:
            if (p.number == number_P):
                return p
        return None
