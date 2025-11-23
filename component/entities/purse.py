import random
from component.entities.static_entity import StaticEntity
from component.position import Position
from component.grid import Grid


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
        self._target_pos = Position(x, y)

        self._position = Position(x, -self._sprite.get_height())

        self._speed = 5
        self._arrived = False

    # TODO animer la bourse qui tombe du ciel
    def update(self):
        if not self._arrived:
            self._position.y += (self._target_pos.y - self._position.y) * 0.1
            if abs(self._position.y - self._target_pos.y) < 1:
                self._position.y = self._target_pos.y
                self._arrived = True

    def draw(self, surface):
        self.update()
        surface.blit(self._sprite, (self._position.x, self._position.y))

    # ------- Getters et Setters -------

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, value: int):
        self._amount = value
