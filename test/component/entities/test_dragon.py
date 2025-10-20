import pytest
import pygame
from unittest.mock import patch, MagicMock

from component.entities.dragon import Dragonnet, DragonMoyen, DragonGeant, Dragon
from component.position import Position

@pytest.fixture(autouse=True)
def mock_pygame(monkeypatch):
    # Mock pygame image loading and subsurface
    mock_surface = MagicMock()
    mock_surface.subsurface.return_value = MagicMock()
    monkeypatch.setattr(pygame.image, "load", lambda path: mock_surface)
    return mock_surface

def test_dragonnet_init():
    d = Dragonnet(1, 2)
    assert d._position.x == 1
    assert d._position.y == 2
    assert d.name == "Dragonnet"
    assert d._attack_damage == 10
    assert d._attack_range == 1
    assert d._cost is not None
    assert d._speed_base == 6

def test_dragonmoyen_init():
    d = DragonMoyen(3, 4)
    assert d._position.x == 3
    assert d._position.y == 4
    assert d.name == "Dragon"
    assert d._attack_damage == 20
    assert d._attack_range == 2
    assert d._cost is not None
    assert d._speed_base == 4

def test_dragongeant_init():
    d = DragonGeant(5, 6)
    assert d._position.x == 5
    assert d._position.y == 6
    assert d.name == "Dragon Géant"
    assert d._attack_damage == 40
    assert d._attack_range == 3
    assert d._cost is not None
    assert d._speed_base == 2

def test_move_dragon_sets_target_and_moving():
    d = Dragonnet(0, 0)
    d.move_dragon(5, 5)
    assert d._target_place.x == 5
    assert d._target_place.y == 5
    assert d._moving is True

def test_reset_speed_sets_actual_speed_and_modifier():
    d = Dragonnet(0, 0)
    d._actual_speed = 2
    d._speed_modifier = 5
    # initialiser _base_speed car la propriété base_speed utilise _base_speed
    d._base_speed = d._speed_base
    d.reset_speed()
    assert d._actual_speed == d.base_speed
    assert d._speed_modifier == 0

def test_update_moves_towards_target(monkeypatch):
    d = Dragonnet(0, 0)
    d.move_dragon(2, 0)
    # Patch Position.move to actually update x/y
    def move(dx, dy):
        d._position.x += dx
        d._position.y += dy
    d._position.move = move
    d._imageSprite = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
    d.update()
    assert d._position.x == 1
    assert d._moving is True
    d.update()
    assert d._position.x == 2
    # Now should stop moving
    d.update()
    assert d._moving is False