# pilote.py

from datetime import time


class Pilote:
    def __init__(self, position, numero, nom, tour):
        self.position = position  # Position dans la course
        self.numero = numero  # Numéro du pilote
        self.nom = nom  # Nom du pilote
        self.tour = tour  # Nombre de tours courant
        self.chronos = [] # liste des temps de passage

    def ajouter_chrono(self, *temps):
        for t in temps:
            chrono = self.convertir_en_time(t)
            if chrono:  # Ajoute uniquement si la conversion a réussi
                self.chronos.append(chrono)
    
    def convertir_en_time(self, horaire):
        try:
            if ":" not in horaire:
                raise ValueError(f"Format invalide: {horaire}")
            h, m = horaire.split(":")
            
            if not h.isdigit() or not m.isdigit():
                raise ValueError(f"Valeurs invalides: {horaire}")
            h, m = int(h), int(m)

            if not (0 <= h < 24 and 0 <= m < 60):  # Vérification des limites
                raise ValueError(f"Valeurs hors limites: {horaire}")
            return time(h, m)
        except ValueError as e:
            # print(f"Erreur : {e}")  # Affichage de l'erreur
            return time(0, 0)  # Retourne 0:0 en cas d'erreur

    # def __str__(self):
    #     tempChronos = ""
    #     for chr in self.chronos.temps_passage:
    #         tempChronos += chr + " / "
    #     return (
    #         f"Position : {self.position}\n"
    #         f"Numéro : {self.numero}\n"
    #         f"Nom pilote : {self.nom}\n"
    #         f"Tour: {self.tour}\n"
    #         f"Chronos: {tempChronos}\n"
    #     )
