# chrono.py

class Chrono:
    def __init__(self):
        self.temps_passage = []

    def ajouter_temps(self, *temps):
        """Ajoute un ou plusieurs temps au chrono."""
        self.temps_passage.extend(temps)  # Ajoute tous les temps donnés à la liste
    
    # def __str__(self):
    #     return (
    #         f"Position : {self.position}\n"
    #     )
