from typing import List

import screen_const as sc
from component.enum.type_entities import TypeEntitiesEnum
from component.position import Position
from const import SPAWN_POS_P1, SPAWN_POS_P2


class Cell:
    """ Cellule de la grille """

    def __init__(self, x, y):
        self._position = Position(x, y)
        self._occupants: List = []

    def remove_occupant(self, occupant=None) -> None:
        """
        Supprime :
        - soit un occupant précis
        - soit tous les occupants si occupant == None
        :param occupant: occupant à supprimer ou None pour tout supprimer
        :return: None
        """
        if occupant is None:
            self._occupants.clear()
        else:
            if occupant in self._occupants:
                self._occupants.remove(occupant)

    def apply_zone_effects_end_turn(self) -> None:
        """
        Applique les effets de zone aux dragons présents dans la cellule en fin de tour
        :return None
        """
        dragons = []
        zones = []

        for occ in self.occupants:
            if TypeEntitiesEnum.DRAGON in occ.type_entity:
                dragons.append(occ)
            if (TypeEntitiesEnum.GOOD_EFFECT_ZONE in occ.type_entity or
                    TypeEntitiesEnum.BAD_EFFECT_ZONE in occ.type_entity):
                zones.append(occ)

        for dragon in dragons:
            dragon.reset_speed()
            for zone in zones:
                zone.effect.apply_effect(dragon)

    def get_pixel_position(self) -> Position:
        """Retourne la position en pixel de la cellule
        :return: Position en pixel
        """
        pixel_x = self.position.x * sc.TILE_SIZE + sc.OFFSET_X
        pixel_y = self.position.y * sc.TILE_SIZE + sc.OFFSET_Y
        return Position(pixel_x, pixel_y)

    @staticmethod
    def get_cell_by_pixel(grid: 'Grid', pixel_pos) -> 'Cell | None':
        """Retourne la cellule correspondant à une position en pixel
        :param grid: Grille de jeu
        :param pixel_pos: Position en pixel (x, y)
        :return: Cellule correspondante ou None si hors grille
        """
        px, py = pixel_pos
        col = (px - sc.OFFSET_X) // sc.TILE_SIZE
        row = (py - sc.OFFSET_Y) // sc.TILE_SIZE

        if not (0 <= col < grid.nb_columns and 0 <= row < grid.nb_rows):
            return None

        return grid.cells[row][col]

    @property
    def occupants(self):
        """return the current occupant"""
        return self._occupants

    @occupants.setter
    def occupants(self, value):
        self._occupants = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def __str__(self):
        """Display the cell"""
        if self._occupants:

            return f"Cell({self.position.x}, {self.position.y}): " + ", ".join(
                occ.name for occ in self._occupants)
        else:
            return f"Cell({self.position.x}, {self.position.y}): Empty"

    def __repr__(self):
        return str(self)


class Grid:
    """Grille de jeu"""

    def __init__(self, nb_columns: int = sc.COLS, nb_rows: int = sc.ROWS):
        self.nb_columns = nb_columns
        self.nb_rows = nb_rows
        self.cells = [[Cell(x, y) for x in range(nb_columns)] for y in range(nb_rows)]

    def add_static_occupants(self, occupant, cell: Cell, width: int, height: int) -> bool:
        """Place un occupant statique sur la grille
        :param occupant: occupant à placer
        :param cell: cellule de départ
        :param width: largeur en cellules
        :param height: hauteur en cellules
        :return: True si placement réussi, False sinon
        """
        x0, y0 = cell.position.x, cell.position.y

        for y in range(y0, y0 + height):
            for x in range(x0, x0 + width):
                if not (0 <= x < self.nb_columns) or not (0 <= y < self.nb_rows):
                    print("Placement hors grille")
                    return False

                cell = self.cells[y][x]
                cell.occupants.append(occupant)
                occupant.position = cell.position

        return True

    def add_occupant(self, occupant, cell: Cell) -> bool:
        """
        Place un occupant sur la grille
        :param occupant: occupant à placer
        :param cell: cellule où placer l'occupant
        :return: True si placement réussi, False sinon
        """

        x = cell.position.x
        y = cell.position.y
        if not (0 <= x < self.nb_columns) or not (0 <= y < self.nb_rows):
            return False
        cell = self.cells[y][x]
        if len(cell.occupants) > 0:
            cell.occupants.append(occupant)
            occupant.cell = cell
        else:
            cell.occupants.append(occupant)

        return True

    def free_cells(self) -> List[Cell]:
        """
        Récupère toutes les cases libres
        :return: Liste des cellules libres
        """
        free_cells = []
        for y in range(self.nb_rows):
            for x in range(self.nb_columns):
                current_cell = self.cells[y][x]
                if (x, y) in [SPAWN_POS_P1, SPAWN_POS_P2]:
                    continue
                if len(current_cell.occupants) == 0:
                    free_cells.append(current_cell)
        return free_cells

    def distance(self, occupant1, occupant2) -> int:
        """Calcule la distance de Manhattan entre deux occupants
        :param occupant1: Premier occupant
        :param occupant2: Second occupant
        :return: Distance de Manhattan
        """
        x1, y1 = occupant1.position.x, occupant1.position.y
        x2, y2 = occupant2.position.x, occupant2.position.y

        return abs(x1 - x2) + abs(y1 - y2)

    def __str__(self):
        """Display the entire grid"""
        return "\n".join(
            " | ".join(str(cell) for cell in row)
            for row in self.cells
        )

    def get_vacant_cells(self) -> List[Cell]:
        """
        Retourne la liste des cellules vides de la grille
        :return: List[Cell]
        """

        vacant_cells = []
        for row in self.cells:
            for cell in row:
                if len(cell.occupants) == 0:
                    vacant_cells.append(cell)
        return vacant_cells

    def get_adjacent_free_cells(self, cell: Cell) -> List[Cell]:
        """
        Retourne la liste des cellules adjacentes libres autour d'une position donnée
        :param cell: Cellule de référence
        :return: List[Cell]
        """
        adjacent_cells = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Gauche, Droite, Haut, Bas
        for dx, dy in directions:
            new_x = cell.position.x + dx
            new_y = cell.position.y + dy
            if 0 <= new_x < sc.COLS and 0 <= new_y < sc.ROWS:
                adjacent_cell = self.cells[new_y][new_x]
                if len(adjacent_cell.occupants) == 0:
                    adjacent_cells.append(adjacent_cell)
        return adjacent_cells

    # ------- Getters et Setters -------
    @property
    def nb_columns(self) -> int:
        return self._nb_columns

    @nb_columns.setter
    def nb_columns(self, value: int):
        self._nb_columns = value

    @property
    def nb_rows(self) -> int:
        return self._nb_rows

    @nb_rows.setter
    def nb_rows(self, value: int):
        self._nb_rows = value

    @property
    def cells(self) -> list:
        return self._cells

    @cells.setter
    def cells(self, value: list):
        self._cells = value
