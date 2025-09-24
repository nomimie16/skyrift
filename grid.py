from component.Position import Position
from component.entities.Dragon import Dragonnet

class Cell:
    """Definition of a grid cell"""

    def __init__(self, x, y):
        self.position = Position(x, y)
        self.occupant = None


    def __str__(self):
        """Display the cell"""
        if self.occupant:
            return f"[{self.occupant.sprite_path}]"
        return str(self.position)

    def __repr__(self):
        return str(self)


class Grid:
    """Definition of a game board grid"""

    def __init__(self, nb_columns, nb_rows):
        self.nb_columns = nb_columns
        self.nb_rows = nb_rows
        self.cells = [
            [Cell(x, y) for x in range(nb_columns)]
            for y in range(nb_rows)
        ]

    def add_occupant(self, occupant, position: Position):
        """Place an occupant (e.g., a dragon) on the grid"""
        x = position.get_x()
        y = position.get_y()

        if not (0 <= x < self.nb_columns) or not (0 <= y < self.nb_rows):
            print(f"Position ({x}, {y}) is out of grid")
            return False
        
        cell = self.cells[y][x]
        if cell.occupant is None:
            cell.occupant = occupant
            occupant.position = cell.position
            return True
        return False

    def __str__(self):
        """Display the entire grid"""
        return "\n".join(
            " | ".join(str(cell) for cell in row)
            for row in self.cells
        )


if __name__ == '__main__':

    pos1 = Position(0, 2)
    pos2 = Position(1, 2)

    # Create the grid
    grid = Grid(3, 3)

    # Test add methode
    grid.add_occupant(Dragonnet(pos1), pos2)
    print(f"Grid 1:\n{grid}")

    # # Test move method (if needed)
    # pos2.move(3, 2)
    # print(f"Position 2 (+3x, +2y): {pos2}")
    # pos3.move(-12, 2)
    # print(f"Position 3 (-12x, +2y): {pos3}")
