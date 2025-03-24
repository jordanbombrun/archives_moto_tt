# rider.py

from datetime import time


class Rider:
    def __init__(self, position, number, name, current_tour):
        self.final_position = position  # Position finale
        self.number = number  # Numéro du pilote
        self.name = name  # Nom du pilote
        self.current_tour = current_tour  # Numéro du tour en cours
        self.chronos_tour_CP = [] # liste des temps de passage, par tour
        self.positions_tour_CP = [] # liste des positions pour chaque CP, par tour

    def add_chrono(self, *chrono_P):
        for t in chrono_P:
            chrono = self.convert_time(t)
            if chrono:  # Ajoute uniquement si la conversion a réussi
                self.chronos_tour_CP[int(self.current_tour)-1].append(chrono)
    
    def add_position(self, *position_P):
        for pos in position_P:
            self.positions_tour_CP[int(self.tour_courant)-1].append(pos)

    def convert_time(self, horaire):
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

    def print_positions(self):
        for index_tour, tour in enumerate(self.positions_tour_CP):
            print(f'Tour {index_tour + 1} :')
            if not tour:
                print('  Aucun CP')
            else:
                for index_cp, cp in enumerate(tour):
                    print(f'  CP {index_cp + 1} : {cp}')
            print('-' * 20)
        print(f'Position finale : {self.final_position}')

