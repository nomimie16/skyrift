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
                         zone_effect=TornadoEffect())
        self._duration = randint(1, 5)  # nombre de tours restants avant disparition
        self._name: str = "Tornade"
        self.type_entity: List[TypeEntitiesEnum] = [TypeEntitiesEnum.TORNADO, TypeEntitiesEnum.EFFECT_ZONE]
        self._target_cell: Cell | None = None
        self._cell: Cell = Cell(x_cell, y_cell)
        self._pixel_pos = Position(
            x_cell * sc.TILE_SIZE + sc.OFFSET_X,
            y_cell * sc.TILE_SIZE + sc.OFFSET_Y
        )
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

    def move_tornado(self):
        """
        Mouvement du dragon
        :return: None
        """
        possible_cells = Grid.get_adjacent_free_cells(self._cell)
        self._target_cell = possible_cells[randint(0, len(possible_cells) - 1)]
        # print(f"Déplacement de la tornade {self.name} vers la cellule ({self._target_cell.position.x}, {self._target_cell.position.y})")
        self._moving = True
        self._cell = self._target_cell
        self.position = Position(self._cell.position.x, self._cell.position.y)

    def update(self):
        """
        Met à jour la position du dragon lors de son déplacement
        :return: None
        """
        self.duration -= 1

        # if not self._moving or not self._target_cell:
        #     return

        target_x = self._target_cell.position.x + sc.OFFSET_X
        target_y = self._target_cell.position.y + sc.OFFSET_Y

        dx = target_x - self._pixel_pos.x
        dy = target_y - self._pixel_pos.y

        if dx != 0:
            step_x = min(0.5, abs(dx)) * (1 if dx > 0 else -1)
            self._pixel_pos.x += step_x
        elif dy != 0:
            step_y = min(0.5, abs(dy)) * (1 if dy > 0 else -1)
            self._pixel_pos.y += step_y

        if self._pixel_pos.x == target_x and self._pixel_pos.y == target_y:
            self._moving = False
            self.grid_pos.x = self._target_cell.x
            self.grid_pos.y = self._target_cell.y
            self._target_cell = None
            self._index_img = 0

        if self._moving:
            self._anim_counter += 1
            if self._anim_counter >= 50:
                self._anim_counter = 0
                self._index_img = (self._index_img + 1) % len(self._imageSprite)

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
