import economy


class Player:  # a completer
    """Classe représentant un joueur (humain ou IA)"""

    def __init__(self, name: str = "Player", color: str="bleu"):
        self._name = name
        self._color = color
        self._economy = economy.Economy()  # economie du joueur
        self._units = []  # unités appartenant au joueur

    def add_unit(self, unit):
        """Ajoute une unité à la liste des unités du joueur"""
        self._units.append(unit)
    def remove_unit(self, idx):
        """Retire une unité de la liste des unités du joueur"""
        del self._units[idx]

    @property
    def units(self):
        return self._units
    
    @units.setter
    def units(self, units):
        self._units = units

    @property
    def economy(self):
        return self._economy
    
    @economy.setter
    def economy(self, economy):
        self._economy = economy

    @property
    def name(self):
        return self._name
    

