import random
from typing import List

from component.entities.base import Base
from component.entities.island_of_life import IslandOfLife
from component.entities.tornado import Tornado
from component.entities.volcano import Volcano
from component.grid import Cell
from component.position import Position


class MapBuilder:
    """
    Classe qui construit la map de départ :
    - Bases fixes (en haut à gauche / bas à droite)
    - Volcan (position aléatoire)
    - Ile de vie (position aléatoire)
    """

    def __init__(self, grid):
        self.grid = grid

        self.base1 = None
        self.base2 = None
        self.volcano = None
        self.life_island = None
        self.tornado = None

    def build_bases(self):
        """
        Place les bases fixes :
        - base1 : haut gauche
        - base2 : bas droite
        """
        self.base1 = Base(1, 1, sprite_path="assets/img/base.png")
        self.grid.add_static_occupants(self.base1, self.base1.cell, self.base1.height, self.base1.width)

        base2_x = self.grid.nb_columns - 5
        base2_y = self.grid.nb_rows - 5
        base2_cell = Cell(base2_x, base2_y)
        self.base2 = Base(base2_x, base2_y, sprite_path="assets/img/base_ennemie.png")
        self.grid.add_static_occupants(self.base2, base2_cell, self.base2.height, self.base2.width)
        # TODO: ajouter base aux joueurs

    def spawn_random_volcano(self):
        """
        Fait spawn un volcan à une position aléatoire
        """
        temp: Volcano = Volcano(0, 0)
        possible_cells: List = []
        for row in self.grid.cells:
            for cell in row:
                if len(cell.occupants) == 0:
                    pos = cell.position
                    if self.can_place_cell(pos, temp.width, temp.height, 3):
                        possible_cells.append(cell)
        if not possible_cells:
            return None

        chosen_cell: Cell = random.choice(possible_cells)

        self.volcano = Volcano(chosen_cell.position.x, chosen_cell.position.y)
        self.grid.add_static_occupants(
            self.volcano,
            chosen_cell,
            self.volcano.width,
            self.volcano.height
        )

    def spawn_random_island_of_life(self):
        """
        Fait spawn une ile de vie à une position aléatoire
        """
        temp = IslandOfLife(0, 0)
        possible_cells = []
        for row in self.grid.cells:
            for cell in row:
                if len(cell.occupants) == 0:
                    pos = cell.position
                    if self.can_place_cell(pos, temp.width, temp.height, 7):
                        possible_cells.append(cell)
        if not possible_cells:
            return None

        chosen_cell = random.choice(possible_cells)

        self.life_island = IslandOfLife(chosen_cell.position.x, chosen_cell.position.y)
        self.grid.add_static_occupants(
            self.life_island,
            chosen_cell,
            self.life_island.width,
            self.life_island.height
        )

    def sapwn_random_tornado(self):
        """
        Fait spawn une tornade à une position aléatoire
        """
        temp = Tornado(0, 0)
        possible_cells = []
        for row in self.grid.cells:
            for cell in row:
                if len(cell.occupants) == 0:
                    pos = cell.position
                    if self.can_place_cell(pos, temp.width, temp.height, 5):
                        possible_cells.append(cell)
        if not possible_cells:
            return None

        chosen_cell = random.choice(possible_cells)

        self.tornado = Tornado(chosen_cell.position.x, chosen_cell.position.y)
        self.grid.add_static_occupants(
            self.tornado,
            chosen_cell,
            self.tornado.width,
            self.tornado.height
        )

    def build_map(self):
        """
        Construit la carte complète :
        - bases fixes
        - volcan aléatoire
        - ile de vie aléatoire
        """
        self.build_bases()
        self.spawn_random_volcano()
        self.spawn_random_island_of_life()
        # self.sapwn_random_tornado()
        return self.grid

    def can_place_cell(self, position: Position, width: int, height: int, min_gap: int = 3):
        """
        Vérifie si un occupant statique peut être placé à la position donnée
        en respectant un gap avec les autres occupants.

        :param position: Position de départ (coin supérieur gauche)
        :param width: largeur de l’occupant
        :param height: hauteur de l’occupant
        :param min_gap: nombre minimal de cases vides entre les bords
        :return: True si l’occupant peut être placé, False sinon
        """
        x0, y0 = position.x, position.y
        target_cells: List = []
        min_dist = None

        for y in range(y0, y0 + height):
            for x in range(x0, x0 + width):
                if not (0 <= x < self.grid.nb_columns) or not (0 <= y < self.grid.nb_rows):
                    return False
                if len(self.grid.cells[y][x].occupants) > 0:
                    return False

        for y in range(y0, y0 + height):
            for x in range(x0, x0 + width):
                target_cells.append((x, y))

        for row in self.grid.cells:
            for cell in row:
                if len(cell.occupants) > 0:
                    ox, oy = cell.position.x, cell.position.y
                    for (tx, ty) in target_cells:
                        dist = abs(tx - ox) + abs(ty - oy)

                        if min_dist is None or dist < min_dist:
                            min_dist = dist
                    gap = min_dist - 1
                    if gap < min_gap:
                        return False

        return True
