class Position:

    def __init__(self, x: int, y: int):
        """x et y sont les coordonnées sr la grille"""
        self._x: int = x
        self._y: int = y

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

    @property
    def x(self) -> int:
        """Retourne le x de la position"""
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        """Définit le x de la position"""
        self._x = value

    @property
    def y(self) -> int:
        """Retourne le y de la position"""
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        """Définit le y de la position"""
        self._y = value

    def __str__(self):
        """Affichage de la position"""
        return f"({self.x}, {self.y})"
