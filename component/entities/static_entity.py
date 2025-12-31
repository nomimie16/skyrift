from typing import List

import pygame

import screen_const as sc
from component.enum.type_entities import TypeEntitiesEnum
from component.grid import Cell
from component.position import Position


class StaticEntity:
    """Classe de base pour les entités statiques (bâtiments, obstacles, zones d'effet, etc.)"""

    def __init__(self, x_cell: int, y_cell: int, name: str, type_entity: List[TypeEntitiesEnum],
                 sprite_path: str | None,
                 width: int,
                 height: int):
        self._cell = Cell(x_cell, y_cell)
        self._pixel_pos = self.cell.get_pixel_position()
        self._name = name
        self._type_entity: List[TypeEntitiesEnum] = type_entity
        self._sprite_path = sprite_path
        if sprite_path:
            self._sprite = pygame.image.load(sprite_path).convert_alpha()
        self._width = width
        self._height = height

    def draw(self, surface) -> None:
        """
        Dessine l'entité statique à l'écran
        :param surface: Surface sur laquelle dessiner l'entité
        :return:
        """
        scaled = pygame.transform.scale(
            self._sprite,
            (self.width * sc.TILE_SIZE, self.height * sc.TILE_SIZE)
        )
        surface.blit(scaled, (self._pixel_pos.x, self._pixel_pos.y))

    @property
    def rect(self) -> pygame.Rect:
        """
        Retourne le rectangle englobant de l'entité statique
        :return:
        """
        return pygame.Rect(self._position.x, self._position.y, self._width, self._height)

    # ------- Getters et Setters -------

    @property
    def cell(self) -> Cell:
        return self._cell

    @cell.setter
    def cell(self, value: Cell) -> None:
        self._cell = value

    @property
    def pixel_pos(self) -> Position:
        return self._pixel_pos

    @pixel_pos.setter
    def pixel_pos(self, value: Position) -> None:
        self._pixel_pos = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name) -> None:
        self._name = name

    @property
    def type_entity(self) -> list[TypeEntitiesEnum]:
        return self._type_entity

    @type_entity.setter
    def type_entity(self, value: List[TypeEntitiesEnum]) -> None:
        self._type_entity = value

    @property
    def sprite_path(self) -> str:
        return self._sprite_path

    @sprite_path.setter
    def sprite_path(self, sprite_path) -> None:
        self._sprite_path = sprite_path

    @property
    def sprite(self) -> pygame.Surface:
        return self._sprite

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width) -> None:
        self._width = width

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, height) -> None:
        self._height = height
