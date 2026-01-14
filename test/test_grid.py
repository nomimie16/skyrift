from src.component.entities.dragon import Dragonnet
from src.component.position import Position
from src.component.grid import Grid, Cell

import pytest

class TestOccupant:
    def __init__(self, name="dummy", width=1, height=1):
        self.name = name
        self.width = width
        self.height = height
        self.cell = None
        self.position = None
        
# Classe de test pour la classe grid
class TestGrid:

    def test_grid_initialization(self):
        grid = Grid(5, 4)
        assert grid.nb_columns == 5
        assert grid.nb_rows == 4
        assert len(grid.cells) == 4
        assert len(grid.cells[0]) == 5

    def test_add_single_occupant(self):
        grid = Grid(5, 5)
        occupant = TestOccupant()
        cell = grid.cells[2][3]

        result = grid.add_occupant(occupant, cell)

        assert result is True
        assert occupant in grid.cells[2][3].occupants

    def test_add_occupant_outside_grid(self):
        grid = Grid(3, 3)
        occupant = TestOccupant()
        fake_cell = Cell(10, 10)

        result = grid.add_occupant(occupant, fake_cell)

        assert result is False

    def test_add_static_occupant_multi_cells(self):
        grid = Grid(5, 5)
        occupant = TestOccupant(width=2, height=2)
        start_cell = grid.cells[1][1]

        result = grid.add_static_occupants(occupant, start_cell, 2, 2)

        assert result is True
        for y in range(1, 3):
            for x in range(1, 3):
                assert occupant in grid.cells[y][x].occupants

        assert occupant.cell == grid.cells[2][2]

    def test_add_static_occupant_outside_grid_fails(self):
        grid = Grid(4, 4)
        occupant = TestOccupant(width=3, height=3)
        start_cell = grid.cells[3][3]

        result = grid.add_static_occupants(occupant, start_cell, 3, 3)

        assert result is False

    def test_free_cells(self):
        grid = Grid(3, 3)
        occupant = TestOccupant()
        grid.add_occupant(occupant, grid.cells[1][1])

        free_cells = grid.free_cells()

        assert grid.cells[1][1] not in free_cells
        assert len(free_cells) == 8

    def test_move_large_occupant(self):
        grid = Grid(6, 6)
        occupant = TestOccupant(width=2, height=2)

        start_cell = grid.cells[1][1]
        grid.add_static_occupants(occupant, start_cell, 2, 2)

        new_cell = grid.cells[3][3]
        grid.move_large_occupant(occupant, new_cell)

        for y in range(3, 5):
            for x in range(3, 5):
                assert occupant in grid.cells[y][x].occupants

        assert occupant.cell == grid.cells[3][3]