from datetime import time
from typing import Optional

from RankingMotoApp.app.models.rider import Rider


class Participation:
    def __init__(
        self,
        final_position: Optional[int] = None,
        number: Optional[int] = None,
        current_lap: int = 0,
        db_id: Optional[int] = None,
        rider: Optional[Rider] = None,
    ):
        self.db_id = db_id
        self.rider = rider  # instance de Rider ou None
        self.final_position = final_position
        self.number = number
        self.current_lap = current_lap
        self.chronos_lap_CP = []      # liste de listes : par tour, liste des chronos
        self.positions_lap_CP = []    # liste de listes : par tour, positions aux CP

    def _ensure_lap_lists(self, lap_index: int):
        # s'assure que les structures pour le tour existent
        while len(self.chronos_lap_CP) <= lap_index:
            self.chronos_lap_CP.append([])
        while len(self.positions_lap_CP) <= lap_index:
            self.positions_lap_CP.append([])

    def add_chrono(self, *chrono_P):
        lap_idx = max(0, int(self.current_lap) - 1)
        self._ensure_lap_lists(lap_idx)
        for t in chrono_P:
            chrono = self.convert_time(t)
            if chrono is not None:
                self.chronos_lap_CP[lap_idx].append(chrono)

    def add_position(self, *position_P):
        lap_idx = max(0, int(self.current_lap) - 1)
        self._ensure_lap_lists(lap_idx)
        for pos in position_P:
            self.positions_lap_CP[lap_idx].append(pos)

    def convert_time(self, horaire: str):
        try:
            if horaire is None:
                return None
            if ":" not in horaire:
                raise ValueError(f"Format invalide: {horaire}")
            parts = horaire.split(":")
            if len(parts) != 2:
                raise ValueError(f"Format invalide: {horaire}")
            h, m = parts
            if not h.isdigit() or not m.isdigit():
                raise ValueError(f"Valeurs invalides: {horaire}")
            h, m = int(h), int(m)
            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError(f"Valeurs hors limites: {horaire}")
            return time(h, m)
        except Exception:
            return None

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

    def format_positions_html(self):
        positions = []
        for index_lap, list_cp in enumerate(self.positions_lap_CP):
            current_lap = index_lap + 1
            if list_cp:
                for index_cp, pos in enumerate(list_cp):
                    if pos is not None:
                        positions.append({
                            'tour': current_lap,
                            'cp': index_cp + 1,
                            'pos': pos
                        })
        return positions