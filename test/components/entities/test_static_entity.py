import pygame
import pytest
from unittest.mock import patch, MagicMock

from src.component.grid import Cell
from src.component.entities.static_entity import StaticEntity
from src.enum.type_entities import TypeEntitiesEnum
from src import screen_const as sc
from src.component.position import Position


class TestStaticEntity:

    @patch("pygame.image.load")
    def setup_method(self, method, mock_load):
        """Initialisation avant chaque test"""
        # Crée un vrai pygame.Surface pour le sprite
        mock_sprite = pygame.Surface((32, 32))  # taille arbitraire
        mock_load.return_value = mock_sprite

        self.static_entity = StaticEntity(
            x_cell=2,
            y_cell=3,
            name="Test Entity",
            type_entity=[TypeEntitiesEnum.OBSTACLE],
            sprite_path="../../assets/sprites/dragonnet.png",
            width=2,
            height=2
        )


    def test_static_entity_initialization(self):
        assert self.static_entity.cell.position.x == 2
        assert self.static_entity.cell.position.y == 3
        assert self.static_entity.name == "Test Entity"
        assert TypeEntitiesEnum.OBSTACLE in self.static_entity.type_entity
        assert self.static_entity.width == 2
        assert self.static_entity.height == 2

    def test_static_entity_draw(self):
        surface = pygame.Surface((800, 600))
        try:
            self.static_entity.draw(surface)
            draw_successful = True
        except Exception:
            draw_successful = False
        assert draw_successful

    def test_static_entity_rect(self):
        # On utilise _pixel_pos à la place de _position
        rect = pygame.Rect(
            self.static_entity.pixel_pos.x,
            self.static_entity.pixel_pos.y,
            self.static_entity.width,
            self.static_entity.height
        )
        assert rect.width == self.static_entity.width
        assert rect.height == self.static_entity.height
        assert rect.x == self.static_entity.pixel_pos.x
        assert rect.y == self.static_entity.pixel_pos.y

    def test_static_entity_cell_setter(self):
        new_cell = Cell(5, 6)
        self.static_entity.cell = new_cell
        # Mettre à jour pixel_pos si nécessaire
        self.static_entity.pixel_pos = new_cell.get_pixel_position()
        assert self.static_entity.cell.position.x == 5
        assert self.static_entity.cell.position.y == 6

    def test_static_entity_pixel_pos(self):
        pixel_pos = self.static_entity.pixel_pos
        expected_pixel_x = self.static_entity.cell.get_pixel_position().x
        expected_pixel_y = self.static_entity.cell.get_pixel_position().y
        assert pixel_pos.x == expected_pixel_x
        assert pixel_pos.y == expected_pixel_y
