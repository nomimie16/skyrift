class Player: # a completer
    """Classe représentant un joueur (humain ou IA)"""

    def __init__(self):
        self.units = []  # unités appartenant au joueur

    def add_unit(self, unit):
        """Ajoute une unité à la liste des unités du joueur"""
        self.units.append(unit)
    
    def remove_unit(self, idx):
        """Retire une unité de la liste des unités du joueur"""
        del self.units[idx]