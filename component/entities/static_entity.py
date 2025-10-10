from component.position import Position
import pygame

class StaticEntity:
    def __init__(self, x: int, y: int, name: str, sprite_path: str, width: int, height: int):
        self._position = Position(x, y)
        self._name = name
        self._sprite_path = sprite_path
        self._sprite = pygame.image.load(sprite_path).convert_alpha()
        self._width = width
        self._height = height

    def draw(self, surface):
        surface.blit(self._sprite, (self._position.x, self._position.y))

    @property
    def rect(self):
        return pygame.Rect(self._position.x, self._position.y, self._width, self._height)

    @property
    def position(self):
        return self._position

    @property
    def name(self):
        return self._name
