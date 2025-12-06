from typing import List

import pygame

import screen_const as sc
from component.enum.type_entities import TypeEntitiesEnum
from component.grid import Cell
from component.position import Position


class StaticEntity:
    def __init__(self, x_cell: int, y_cell: int, name: str, type_entity: List[TypeEntitiesEnum], sprite_path: str,
                 width: int,
                 height: int):
        self._cell = Cell(x_cell, y_cell)
        self._pixel_pos = self.cell.get_pixel_position()
        self._name = name
        self._type_entity: List[TypeEntitiesEnum] = type_entity
        self._sprite_path = sprite_path
        self._sprite = pygame.image.load(sprite_path).convert_alpha()
        self._width = width
        self._height = height

    def draw(self, surface):
        scaled = pygame.transform.scale(
            self._sprite,
            (self.width * sc.TILE_SIZE, self.height * sc.TILE_SIZE)
        )
        surface.blit(scaled, (self._pixel_pos.x, self._pixel_pos.y))

    @property
    def rect(self):
        return pygame.Rect(self._position.x, self._position.y, self._width, self._height)

    # ------- Getters et Setters -------

    @property
    def cell(self) -> Cell:
        return self._cell

    @cell.setter
    def cell(self, value: Cell):
        self._cell = value

    @property
    def pixel_pos(self) -> Position:
        return self._pixel_pos

    @cell.setter
    def cell(self, value: Position):
        self._pixel_pos = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def type_entity(self) -> list[TypeEntitiesEnum]:
        return self._type_entity

    @type_entity.setter
    def type_entity(self, value: List[TypeEntitiesEnum]):
        self._type_entity = value

    @property
    def sprite_path(self):
        return self._sprite_path

    @sprite_path.setter
    def sprite_path(self, sprite_path):
        self._sprite_path = sprite_path

    @property
    def sprite(self):
        return self._sprite

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
