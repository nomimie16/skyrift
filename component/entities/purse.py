import random

import pygame

import screen_const as sc
from component.entities.purse_effect import PurseEffect
from component.entities.zone_entity import ZoneEntity
from component.enum.type_entities import TypeEntitiesEnum
from component.grid import Grid
from component.position import Position


def spawn_random_purse(grid: Grid, amount: int = 50):
    """
    Fait spawn une bourse à une position aléatoire
    :return:
    """
    free_cells = grid.free_cells()
    cell = random.choice(free_cells)
    purse = Purse(cell.position.x, cell.position.y, amount)
    grid.add_occupant(purse, cell)
    return purse


class Purse(ZoneEntity):
    def __init__(self, x_cell: int, y_cell: int, amount: int = 50):
        super().__init__(x_cell, y_cell,
                         sprite_path="assets/sprites/purse.png", width=1, height=1,
                         type_entity=[TypeEntitiesEnum.EFFECT_ZONE, TypeEntitiesEnum.PLAYER_EFFECT_ZONE],
                         zone_effect=PurseEffect())
        self.name = "Bourse"
        self._amount: int = amount
        self._target_pos = Position(y_cell, y_cell)

        # self._speed = 5
        # self._arrived = False

    # TODO animer la bourse qui tombe du ciel
    # def update(self):
    #     if not self._arrived:
    #         self._position.y += (self._target_pos.y - self._position.y) * 0.1
    #         if abs(self._position.y - self._target_pos.y) < 1:
    #             self._position.y = self._target_pos.y
    #             self._arrived = True

    def draw(self, surface):
        scaled_width = int(self.width * sc.TILE_SIZE * 2)
        scaled_height = int(self.height * sc.TILE_SIZE * 2)
        scaled_sprite = pygame.transform.scale(self._sprite, (scaled_width, scaled_height))

        x = self._pixel_pos.x - (scaled_width - sc.TILE_SIZE) // 2
        y = self._pixel_pos.y - (scaled_height - sc.TILE_SIZE)

        surface.blit(scaled_sprite, (x, y))

    # ------- Getters et Setters -------

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, value: int):
        self._amount = value
