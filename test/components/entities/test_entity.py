from unittest.mock import patch, MagicMock

import pytest

from component.entities.entity import Entity
from component.enum.type_entities import TypeEntitiesEnum


@pytest.fixture
def mock_pygame():
    """Mock pygame.image.load pour éviter les FileNotFoundError."""
    with patch("pygame.image.load", return_value=MagicMock()) as mock_load:
        yield mock_load


@pytest.fixture
def entity(mock_pygame):
    return Entity(
        x=2,
        y=3,
        name="TestEntity",
        type_entity=[TypeEntitiesEnum.OBSTACLE],
        max_hp=100,
        attack_damage=20,
        attack_range=2,
        sprite_path="fake/path.png"
    )


def test_entity_initialization(entity):
    assert entity.name == "TestEntity"
    assert entity.hp == 100
    assert entity.max_hp == 100
    assert entity.attack_damage == 20
    assert entity.attack_range == 2
    assert entity.cell.position.x == 2
    assert entity.cell.position.y == 3


def test_take_damage(entity):
    entity.take_damage(30)
    assert entity.hp == 70


def test_take_damage_cannot_go_below_zero(entity):
    entity.take_damage(999)
    assert entity.hp == 0


def test_is_dead(entity):
    entity.take_damage(100)
    assert entity.is_dead() is True


def test_attack(entity, mock_pygame):
    target = Entity(0, 0, "Target", [TypeEntitiesEnum.OBSTACLE],
                    50, 10, 1, "fake/path.png")

    entity.attack(target)
    assert target.hp == 30


def test_hp_setter(entity):
    entity.hp = 200
    assert entity.hp == 100


def test_hp_cannot_be_negative(entity):
    entity.hp = -50
    assert entity.hp == 0


def test_attack_damage_setter(entity):
    entity.attack_damage = 99
    assert entity.attack_damage == 99


def test_sprite_path_setter_loads_new_image(entity, mock_pygame):
    entity.sprite_path = "another/path.png"
    assert entity.sprite_path == "another/path.png"
    mock_pygame.assert_called()
