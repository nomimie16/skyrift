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
        self.y += y

    def get_x(self):
        """Retourne le x de la position"""
        return self.x

    def get_y(self):
        """Retourne le y de la position"""
        return self.y

    def __str__(self):
        """Affichage de la position"""
        return f"({self.x}, {self.y})"

