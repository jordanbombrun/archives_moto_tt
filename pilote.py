# pilote.py

from datetime import time


class Pilote:
    def __init__(self, position, numero, nom, tour_courant):
        self.position = position  # Position dans la course
        self.numero = numero  # Numéro du pilote
        self.nom = nom  # Nom du pilote
        self.tour_courant = tour_courant  # Numéro du tour en cours
        self.chronos_tour_CP = [] # liste des temps de passage, par tour
        self.positions_tour_CP = [] # liste des positions pour chaque CP, par tour

    def ajouter_chrono(self, *chrono_P):
        for t in chrono_P:
            chrono = self.convertir_en_time(t)
            if chrono:  # Ajoute uniquement si la conversion a réussi
                self.chronos_tour_CP[int(self.tour_courant)-1].append(chrono)
    
    def ajouter_position(self, *position_P):
        for pos in position_P:
            self.positions_tour_CP[int(self.tour_courant)-1].append(pos)

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
