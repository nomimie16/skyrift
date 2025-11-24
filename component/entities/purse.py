import random

from component.entities.static_entity import StaticEntity
from component.grid import Grid
from component.position import Position
from screen_const import TILE_SIZE


def spawn_random_purse(grid: Grid, amount: int = 50):
    """
    Fait spawn une bourse à une position aléatoire
    :return:
    """
    free_cells = [
        (x, y)
        for y in range(grid.nb_rows)
        for x in range(grid.nb_columns)
    ]
    x, y = random.choice(free_cells)
    purse = Purse(x, y, amount)
    grid.add_occupant(purse, Position(x, y))
    return purse


class Purse(StaticEntity):
    def __init__(self, x_cell: int, y_cell: int, amount: int):
        super().__init__(x_cell, y_cell, name="Bourse", sprite_path="assets/sprites/purse.png", width=1, height=1)
        self._amount: int = 50
        self._target_pos = Position(y_cell, y_cell)

        self._position = Position(x_cell, -self._sprite.get_height())

        self._speed = 5
        self._arrived = False

        self.grid_pos = Position(x_cell, y_cell)  # position sur la grille
        self._pixel_pos = Position(x_cell * TILE_SIZE, y_cell * TILE_SIZE)  # position pour l'affichage

    # TODO animer la bourse qui tombe du ciel
    def update(self):
        if not self._arrived:
            self._position.y += (self._target_pos.y - self._position.y) * 0.1
            if abs(self._position.y - self._target_pos.y) < 1:
                self._position.y = self._target_pos.y
                self._arrived = True

    def draw(self, surface):
        self.update()
        surface.blit(self._sprite, (self._pixel_pos.x, self._pixel_pos.y))

    # ------- Getters et Setters -------

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, value: int):
        self._amount = value
