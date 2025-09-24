class Position:

    def __init__(self, x, y):
        """x et y sont les coordonnées sr la grille"""
        self.x = x
        self.y = y

    def move(self, x, y):
        """Retourne nouvelle position après déplacement"""
        return Position(self.x + x, self.y + y)