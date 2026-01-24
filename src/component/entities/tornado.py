from random import randint

import pygame

from src import screen_const as sc
from src.component.entities.tornado_effect import TornadoEffect
from src.component.entities.zone_entity import ZoneEntity
from src.component.grid import Cell
from src.component.grid import Grid
from src.component.path_finding import find_path
from src.component.position import Position
from src.enum.type_entities import TypeEntitiesEnum


class Tornado(ZoneEntity):
    """
    Tornade qui se déplace aléatoirement sur la grille
    """

    def __init__(self, x_cell: int, y_cell: int, width: int = 3, height: int = 4):
        super().__init__(x_cell, y_cell, sprite_path="src/assets/sprites/tornade.png", width=width, height=height,
                         type_entity=[TypeEntitiesEnum.EFFECT_ZONE, TypeEntitiesEnum.BAD_EFFECT_ZONE,
                                      TypeEntitiesEnum.TORNADO],
                         zone_effect=TornadoEffect())
        self._duration = randint(2, 10)  # nombre de tours restants avant disparition
        self._pause_duration = 0
        self._name: str = "Tornade"
        self._target_cell: Cell | None = None
        self._index_img: int = 0
        self._sprite_sheet = pygame.image.load(self.sprite_path)
        self._imageSprite = [self._sprite_sheet.subsurface(x * 64, 0, 64, 64) for x in range(4)]
        self._moving = False
        self._anim_counter = 0
        self._path = []
        self._active = True

    def handle_turn(self, grid: Grid) -> None:
        """
        Gestion d'un tour avec la tornade
        :param grid:
        :return:
        """
        if self._active:
            self.move_tornado(grid)
            if self.duration > 0:
                self.duration -= 1

            if self.duration <= 0:
                self.tornado_disable(grid)
                self._pause_duration = randint(3, 4)
        else:
            if self._pause_duration > 0:
                self._pause_duration -= 1
            if self._pause_duration == 0:
                free_cells = grid.free_cells()
                if free_cells:
                    target_cell = free_cells[randint(0, len(free_cells) - 1)]
                    self.cell = target_cell
                    self.tornado_activation(grid)
                    self.duration = randint(2, 10)

    def tornado_activation(self, grid: Grid) -> None:
        """
        Activation de la tornade
        :param grid: Grille sur laquelle est la tornade
        :return: None
        """
        if self._active:
            return

        self._active = True
        grid.add_static_occupants(self, self.cell, self.width, self.height)

    def tornado_disable(self, grid: Grid) -> None:
        """
        Désactivation de la tornade, elle est supprimer temporairement de la grille
        :param grid: grille sur laquelle est la tornade
        :return:
        """
        if self._active:
            self._active = False
            grid.remove_large_occupant(self)

    def move_tornado(self, grid: Grid) -> None:
        """
        Mouvement du dragon
        :param grid: Grille sur laquelle la tornade se déplace
        :return: None
        """
        if self._moving:
            return

        target = grid.get_random_target_cell(self.cell, 3, self.width, self.height)
        if not target:
            return

        self.path = find_path(grid, self.cell, target)
        if self.path:
            self._moving = True

        self.duration -= 1

    def update(self, grid: Grid) -> Grid | None:
        """
        Mise à jour de la position de la tornade
        :param grid: Grille sur laquelle la tornade se déplace
        :return: Grille mise à jour ou None
        """
        if not self._moving:
            return

        target_cell = self.path[0]

        target_px = Position(
            target_cell.position.x * sc.TILE_SIZE + sc.OFFSET_X,
            target_cell.position.y * sc.TILE_SIZE + sc.OFFSET_Y
        )

        dx = target_px.x - self._pixel_pos.x
        dy = target_px.y - self._pixel_pos.y
        moved = False

        if dx != 0:
            moved = True
            self._pixel_pos.x += min(1, abs(dx)) * (1 if dx > 0 else -1)

        if dy != 0:
            moved = True
            self._pixel_pos.y += min(1, abs(dy)) * (1 if dy > 0 else -1)

        if not moved or (abs(dx) <= 4 and abs(dy) <= 4):
            self._pixel_pos.x = target_px.x
            self._pixel_pos.y = target_px.y

            grid.move_large_occupant(self, target_cell)

            self.path.pop(0)
            if not self.path:
                self._moving = False
                self._anim_counter = 0

        self._anim_counter += 1
        if self._anim_counter >= 15:
            self._anim_counter = 0
            self._index_img = (self._index_img + 1) % len(self._imageSprite)
        return grid

    def draw(self, surface) -> None:
        """
        Affichage de la tornade
        :param surface: Surface sur laquelle la tornade se déplace
        :return: None
        """
        if self._active:
            pixel_x = self.cell.position.x * sc.TILE_SIZE + sc.OFFSET_X
            pixel_y = self.cell.position.y * sc.TILE_SIZE + sc.OFFSET_Y

            scaled = pygame.transform.scale(
                self._imageSprite[self._index_img],
                (self.width * sc.TILE_SIZE, self.height * sc.TILE_SIZE)
            )
            surface.blit(scaled, (pixel_x, pixel_y))

    # ------- Getters et Setters -------
    @property
    def duration(self) -> int:
        return self._duration

    @duration.setter
    def duration(self, value: int) -> None:
        self._duration = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value

    @property
    def pause_duration(self) -> int:
        return self._pause_duration

    @pause_duration.setter
    def pause_duration(self, value: int) -> None:
        self._pause_duration = value
