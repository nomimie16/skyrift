from unittest.mock import MagicMock, patch

import pytest

from src import screen_const as sc
from src.component.entities.dragon import Dragonnet, DragonMoyen, DragonGeant, Dragon
from src.component.grid import Grid
from src.component.position import Position


@pytest.fixture
def grid():
    grid = Grid(nb_columns=15, nb_rows=15)
    return grid


@pytest.fixture
def dragons():
    with patch("pygame.image.load", return_value=MagicMock()) as mock_load:
        d1: Dragonnet = Dragonnet(0, 0)
        d2: DragonMoyen = DragonMoyen(5, 5)
        d3: DragonGeant = DragonGeant(10, 10)
        return [d1, d2, d3]


def test_initial_stats(dragons: list[Dragon]):
    # Test des stats initiales
    d1, d2, d3 = dragons
    assert d1.hp == 50
    assert d2.hp == 120
    assert d3.hp == 250

    assert d1.actual_speed == 6
    assert d2.actual_speed == 4
    assert d3.actual_speed == 2


def test_move_dragon_sets_target_cell(dragons, grid):
    d1, d2, d3 = dragons
    d1.move_dragon(3, 3, grid)
    d2.move_dragon(7, 7, grid)
    d3.move_dragon(12, 12, grid)

    assert d1.moving is True
    assert d1._target_cell == grid.cells[3][3]


def test_reset_speed(dragons):
    d1: Dragon = dragons[0]
    d1.speed_modifier = 2
    d1.reset_speed()
    assert d1.actual_speed == d1.speed_base
    assert d1.speed_modifier == 0


def test_update_direction_changes_sprite():
    with patch("pygame.image.load", return_value=MagicMock()), \
            patch("os.path.exists", return_value=True):  # Forcer à True
        d: Dragon = Dragonnet(0, 0)
        old_path = d._sprite_path
        d.update_direction("gauche")
        assert "gauche" in d._sprite_path
        assert d._sprite_path != old_path


def test_update_movement_logic(grid: Grid, dragons: list[Dragon]):
    for d in dragons:
        d._pixel_pos = Position(
            d.cell.position.x * sc.TILE_SIZE + sc.OFFSET_X,
            d.cell.position.y * sc.TILE_SIZE + sc.OFFSET_Y
        )
    d1: Dragon = dragons[0]
    d1.move_dragon(0, 1, grid)
    d1._actual_speed = 1
    initial_y = d1._pixel_pos.y
    d1.update(grid)
    assert d1._pixel_pos.y != initial_y


def test_cost_and_attack_properties(dragons: list[Dragon]):
    d1, d2, d3 = dragons
    assert d1.cost > 0
    assert d2.attack_damage > 0
    assert d3.attack_range > 0


def test_string_representation(dragons: list[Dragon]):
    d1: Dragon = dragons[0]
    s: str = str(d1)
    assert isinstance(s, str)
