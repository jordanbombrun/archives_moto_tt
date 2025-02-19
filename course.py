# course.py

from datetime import date

class Course:
    def __init__(self, nom, date = date(2000, 1, 1), type = "inconnu", nb_CP = 0, nb_tours = 0) :
        self.nom = nom
        self.date = date
        self.type = type # enum : enduro classique, endurance cross, course à CP
        self.pilotes = [] # liste des pilotes
        self.nb_CP = nb_CP
        self.nb_tours = nb_tours

    def ajouter_pilotes(self, pilotes_P):
        self.pilotes.extend(pilotes_P)  # Ajoute tous les pilotes à la liste

    def get_pilote_by_number(self, number_P):
        for p in self.pilotes:
            if (p.number == number_P):
                return p
