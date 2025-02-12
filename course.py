# course.py

from datetime import date

class Course:
    def __init__(self, nom, date = date(2000, 1, 1), type = "inconnu", nb_CP = 0) :
        self.nom = nom
        self.date = date
        self.type = type # enum : enduro classique, endurance cross, course à CP
        self.pilotes = [] # liste des pilotes
        self.nb_CP = nb_CP

    def ajouter_pilotes(self, pilotes_P):
        self.pilotes.extend(pilotes_P)  # Ajoute tous les pilotes à la liste
