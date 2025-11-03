# rider.py

from datetime import time


class Rider:
    def __init__(self, name: str, db_id: int = None):
        self.db_id = db_id  # identifiant en base, None si non renseigné
        self.name = name
        self.participations = []  # liste d'objets Participation

    def add_participation(self, participation):
        # évite les doublons simples
        if participation not in self.participations:
            self.participations.append(participation)
            # lien bidirectionnel si l'objet Participation contient un attribut rider
            try:
                participation.rider = self
            except Exception:
                pass

    def add_chrono(self, *chrono_P):
        for t in chrono_P:
            chrono = self.convert_time(t)
            if chrono:  # Ajoute uniquement si la conversion a réussi
                self.chronos_lap_CP[int(self.current_lap)-1].append(chrono)
    
    def add_position(self, *position_P):
        for pos in position_P:
            self.positions_lap_CP[int(self.current_lap)-1].append(pos)

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

    # affichage des positions du pilote dans le terminal
    def print_positions_cli(self):
        for index_lap, cp in enumerate(self.positions_lap_CP):
            print(f'Tour {index_lap + 1} :')
            if not cp:
                print('  Aucun CP')
            else:
                for index_cp, pos in enumerate(cp):
                    print(f'  CP {index_cp + 1} : {pos}')
            print('-' * 20)
        print(f'Position finale : {self.final_position}')

    # affichage des positions du pilote dans la page html
    def format_positions_html(self):
        positions = []
        for index_lap, list_cp in enumerate(self.positions_lap_CP):
            current_lap = '99'
            current_cp = '99'   
            current_pos = '999'
            current_lap = index_lap + 1
            if list_cp:
                for index_cp, pos in enumerate(list_cp):
                    current_cp = index_cp + 1
                    if pos :
                        positions.append({
                            'tour' : current_lap, 
                            'cp' : current_cp, 
                            'pos' : pos})
        return positions
