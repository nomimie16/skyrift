class Position:

    def __init__(self, x : int, y : int):
        """x et y sont les coordonnées sr la grille"""
        self.x : int = x
        self.y : int = y

    def move(self, x: int, y: int) -> None:
        """
        Déplace la position actuelle de la position
        Args:
            x (int): Décalage horizontal à ajouter à la coordonnée x
            y (int): Décalage vertical à ajouter à la coordonnée y
        Returns:
            None: Met à jour l'objet Position directement
        """
        self.x += x
        self.y += self.y + y

    def get_x(self):
        """Retourne le x de la position"""
        return self.x

    def get_y(self):
        """Retourne le y de la position"""
        return self.y

    def __str__(self):
        """Affichage de la position"""
        return f"({self.x}, {self.y})"


if __name__ == '__main__':

    # Création de positions
    pos1 = Position(0, 0)
    pos2 = Position(5, 10)
    pos3 = Position(12, 3)

    print("Position initiale")
    print(f"Postion 1 : {pos1}")
    print(f"Postion 2 : {pos2}")
    print(f"Postion 3 : {pos3}")

    # Modification de la position
    print("Test mèthode move")
    pos2.move(3,2)
    print(f"Postion 2 (+3x -2y): {pos2}")
    pos3.move(-12,2)
    print(f"Postion 3 (-12x, +2y): {pos3}")

