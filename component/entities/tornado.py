from random import randint

import pygame

import screen_const as sc
from component.entities.tornado_effect import TornadoEffect
from component.entities.zone_entity import ZoneEntity
from component.enum.type_entities import TypeEntitiesEnum
from component.grid import Cell
from component.grid import Grid
from component.position import Position


class Tornado(ZoneEntity):
    def __init__(self, x_cell: int, y_cell: int, width: int = 1, height: int = 1):
        super().__init__(x_cell, y_cell, sprite_path="assets/sprites/dragonnet.png", width=width, height=height,
                         type_entity=[TypeEntitiesEnum.EFFECT_ZONE, TypeEntitiesEnum.BAD_EFFECT_ZONE,
                                      TypeEntitiesEnum.TORNADO],
                         zone_effect=TornadoEffect())
        self._duration = randint(1, 5)  # nombre de tours restants avant disparition
        self._name: str = "Tornade"
        self._target_cell: Cell | None = None
        self._index_img: int = 0
        self._sprite_sheet = pygame.image.load(self.sprite_path)
        self._imageSprite = [self._sprite_sheet.subsurface(x * 64, 0, 64, 64) for x in range(4)]
        self._moving = False
        self._anim_counter = 0

    #
    # def update(self):
    #     """Appeler à chaque tour : diminue la durée de vie de la tornade."""
    #     self.duration -= 1
    #     # return self.duration > 0

    def move_tornado(self, grid: Grid):
        """
        Mouvement du dragon
        :return: None
        """
        possible_cells = grid.get_adjacent_free_cells(self._cell)
        if possible_cells:
            print("Déplacement de la tornade", possible_cells)
            self._target_cell = possible_cells[randint(0, len(possible_cells) - 1)]
            self._moving = True

    def update(self, grid: Grid):
        if not self._moving or not self._target_cell:
            return

        target_px = Position(
            self._target_cell.position.x * sc.TILE_SIZE + sc.OFFSET_X,
            self._target_cell.position.y * sc.TILE_SIZE + sc.OFFSET_Y
        )

        dx = target_px.x - self._pixel_pos.x
        dy = target_px.y - self._pixel_pos.y
        moved = False

        if dx != 0:
            moved = True
            self._pixel_pos.x += min(4, abs(dx)) * (1 if dx > 0 else -1)

        if dy != 0:
            moved = True
            self._pixel_pos.y += min(4, abs(dy)) * (1 if dy > 0 else -1)

        if not moved or (abs(dx) <= 4 and abs(dy) <= 4):
            self._moving = False

            if self._cell:
                self._cell.remove_occupant(self)

            self._cell = self._target_cell
            self._cell.occupants.append(self)

            self._target_cell = None
            self._index_img = 0
        return grid

    def draw(self, surface):
        """
        Affichage de la tornade
        @:param surface: Surface sur laquelle la tornade se déplace
        """

        surface.blit(
            self._imageSprite[self._index_img],
            (
                int(self._pixel_pos.x + (sc.TILE_SIZE - self._imageSprite[self._index_img].get_width()) / 2),
                int(self._pixel_pos.y + (sc.TILE_SIZE - self._imageSprite[self._index_img].get_height()) / 2)
            )
        )

    # ------- Getters et Setters -------
    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value: int):
        self._duration = value
