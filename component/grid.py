from typing import List

import screen_const as sc
from component.position import Position


class Cell:
    """Definition of a grid cell"""

    def __init__(self, x, y):
        self._position = Position(x, y)
        self._occupants: List = []

    def remove_occupant(self, occupant=None):
        """
        Supprime :
        - soit un occupant précis
        - soit tous les occupants si occupant == None
        """
        if occupant is None:
            self._occupants.clear()
        else:
            if occupant in self._occupants:
                self._occupants.remove(occupant)

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
            return "occupe"
        return str(self._position)

    def __repr__(self):
        return str(self)


class Grid:
    """Game board grid"""

    def __init__(self, nb_columns: int = sc.COLS, nb_rows: int = sc.ROWS):
        self.nb_columns = nb_columns
        self.nb_rows = nb_rows
        self.cells = [[Cell(x, y) for x in range(nb_columns)] for y in range(nb_rows)]

    def add_static_occupants(self, occupant, position: Position, width: int, height: int):
        """Place un occupant statique sur la grille"""
        x0, y0 = position.x, position.y

        for y in range(y0, y0 + height):
            for x in range(x0, x0 + width):
                if not (0 <= x < self.nb_columns) or not (0 <= y < self.nb_rows):
                    print("Placement hors grille")
                    return False

                cell = self.cells[y][x]
                cell.occupants.append(occupant)
                occupant.position = cell.position

        return True

    def add_occupant(self, occupant, position: Position):
        """Place an occupant (e.g., a dragon) on the grid"""
        x = position.x
        y = position.y
        if not (0 <= x < self.nb_columns) or not (0 <= y < self.nb_rows):
            print(f"Position ({x}, {y}) is out of grid")
            return False
        cell = self.cells[y][x]
        if len(cell.occupants) > 0:
            cell.occupants.append(occupant)
            occupant.position = cell.position
        else:
            cell.occupants.append(occupant)
            print("Occupant placed at", cell.occupants)
            print(f"Cell ({x}, {y}) is already occupied")
        return True

    def remove_occupant(self, position: Position, occupant=None):
        """
        Supprime :
        - soit un occupant précis
        - soit tous les occupants si occupant == None
        """
        cell = self.cells[position.y][position.x]
        if occupant is None:
            self._occupants.clear()
        else:
            if occupant in cell.occupants:
                cell.occupants.remove(occupant)

    def distance(self, occupant1, occupant2):
        x1, y1 = occupant1.position.x, occupant1.position.y
        x2, y2 = occupant2.position.x, occupant2.position.y

        return abs(x1 - x2) + abs(y1 - y2)

    def __str__(self):
        """Display the entire grid"""
        return "\n".join(
            " | ".join(str(cell) for cell in row)
            for row in self.cells
        )

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
