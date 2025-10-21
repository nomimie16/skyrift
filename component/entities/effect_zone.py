import pygame
from component.position import Position

class EffectZone: # TODO : finir

    def __init__(self, x: int, y: int, name: str, sprite_path: str, width: int, height: int):
        self.name = name
        self.heigth = height
        self.width = width
        self.position = Position(x, y)
        self.sprite = pygame.image.load(sprite_path).convert_alpha()

    @property
    def rect(self):
        return pygame.Rect(self.position.x, self.position.y, self.width, self.heigth)