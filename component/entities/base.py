import pygame

import screen_const as sc
from component.entities.entity import Entity
from component.enum.type_entities import TypeEntitiesEnum


class Base(Entity):
    def __init__(self, x: int, y: int, sprite_path: str | None = None, player=None):
        super().__init__(x, y, name="Base", type_entity=[TypeEntitiesEnum.BASE, TypeEntitiesEnum.OBSTACLE], max_hp=2000,
                         attack_damage=0, attack_range=0,
                         sprite_path=sprite_path)
        self.width = 4
        self.height = 4
        self._player: Player = player

    def draw(self, surface) -> None:
        """
        Dessine la base à l'écran
        :param surface: Surface sur laquelle dessiner la base
        :return: None
        """
        pixel_x = (self.cell.position.x - (self.width - 1)) * sc.TILE_SIZE + sc.OFFSET_X
        pixel_y = (self.cell.position.y - (self.height - 1)) * sc.TILE_SIZE + sc.OFFSET_Y

        scaled = pygame.transform.scale(
            self._sprite,
            (self.width * sc.TILE_SIZE, self.height * sc.TILE_SIZE)
        )

        surface.blit(scaled, (pixel_x, pixel_y))
        self.draw_health_bar(surface, self.width)

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value) -> None:
        self._player = value
