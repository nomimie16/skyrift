import screen_const as sc
from component.position import Position


class Cell:
    """Definition of a grid cell"""

    def __init__(self, x, y):
        self._position = Position(x, y)
        self._occupant = None

    @property
    def occupant(self):
        """return the current occupant"""
        return self._occupant

    @occupant.setter
    def occupant(self, value):
        self._occupant = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def __str__(self):
        """Display the cell"""
        if self._occupant:
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

    def add_static_occupants(self, occupant, position: Position, height: int, width: int):
        """Place un occupant non mobile sur la grille"""
        x_start = position.get_x()
        y_start = position.get_y()
        for y in range(y_start, y_start + height):
            for x in range(x_start, x_start + width):
                if not (0 <= x < self.nb_columns) or not (0 <= y < self.nb_rows):
                    print(f"Position ({x}, {y}) is out of grid")
                    return False
                cell = self.cells[y][x]
                if cell._occupant is None:
                    cell._occupant = occupant
                    occupant.position = cell._position
                else:
                    print(f"Cell ({x}, {y}) is already occupied")
                    return False
        return True

    def add_occupant(self, occupant, position: Position):
        """Place an occupant (e.g., a dragon) on the grid"""
        x = position.get_x()
        y = position.get_y()
        if not (0 <= x < self.nb_columns) or not (0 <= y < self.nb_rows):
            print(f"Position ({x}, {y}) is out of grid")
            return False
        cell = self.cells[y][x]
        if cell._occupant is None:
            cell._occupant = occupant
            occupant.position = cell._position
            return True
        return False

    def remove_occupant(self, position: Position):
        """Place an occupant (e.g., a dragon) on the grid"""
        cell = self.cells[position.get_y()][position.get_x()]
        if cell._occupant is not None:
            cell._occupant = None

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
