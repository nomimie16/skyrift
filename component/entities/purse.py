import random

from component.entities.static_entity import StaticEntity
from component.position import Position
from grid import Grid


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
    def __init__(self, x: int, y: int, amount: int):
        super().__init__(x, y, name="Bourse", sprite_path="assets/sprites/purse.png", width=1, height=1)
        self._amount: int = 50
        self._position = Position(x, y)

    # ------- Getters et Setters -------

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, value: int):
        self._amount = value
