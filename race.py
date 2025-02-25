# course.py

from datetime import date

class Race:
    def __init__(self, name, date = date(2000, 1, 1), type = "inconnu", nb_CP = 0, nb_tours = 0) :
        self.name = name
        self.date = date
        self.type = type # enum : enduro classique, endurance cross, course à CP
        self.pilotes = [] # liste des pilotes
        self.nb_CP = nb_CP # nb CP par tour
        self.nb_tours = nb_tours # nb tours

    def add_pilotes(self, pilotes_P):
        self.pilotes.extend(pilotes_P)  # Ajoute tous les pilotes à la liste

    def get_pilote_by_number(self, number_P):
        for p in self.pilotes:
            if (p.number == number_P):
                return p
        return None
