# pilote.py

from chrono import Chrono


class Pilote:
    def __init__(self, position, numero, nom, tour):
        self.position = position  # Position dans la course
        self.numero = numero  # Numéro du pilote
        self.nom = nom  # Nom du pilote
        self.tour = tour  # Nombre de tours courant
        self.chronos = Chrono()

    def __str__(self):
        tempChronos = ""
        for chr in self.chronos.temps_passage:
            tempChronos += chr + " / "
        return (
            f"Position : {self.position}\n"
            f"Numéro : {self.numero}\n"
            f"Nom pilote : {self.nom}\n"
            f"Tour: {self.tour}\n"
            f"Chronos: {tempChronos}\n"
        )
