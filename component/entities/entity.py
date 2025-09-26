import pygame

from component.Position import Position


class Entity:
    def __init__(self, x, y, max_hp, sprite_path):
        self._position = Position(x, y)
        self._max_hp = max_hp
        self._hp = max_hp
        self._sprite = pygame.image.load(sprite_path).convert_alpha()

    def draw(self, surface):
        surface.blit(self._sprite, (self._position.x, self._position.y))

    def take_damage(self, amount):
        self._hp = max(0, self._hp - amount)

    def is_dead(self):
        return self._hp <= 0
