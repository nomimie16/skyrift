import pygame

from component.position import Position


class Entity:
    def __init__(self, x: int, y: int, name: str, max_hp: int, sprite_path: str):
        self._position: Position = Position(x, y)
        self._name: str = name
        self._max_hp: int = max_hp
        self._hp: int = max_hp
        self._sprite = pygame.image.load(sprite_path).convert_alpha()

    def draw(self, surface):
        """
        Affichage d'une entité
        @:param surface: Surface sur laquelle l'entité est placée
        """
        surface.blit(self._sprite, (self._position.x, self._position.y))

    def take_damage(self, amount):
        self._hp = max(0, self._hp - amount)

    def is_dead(self):
        return self._hp <= 0

    # ------- Getters et Setters -------

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, value: Position):
        self._position = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def max_hp(self) -> int:
        return self._max_hp

    @max_hp.setter
    def max_hp(self, value: int):
        self._max_hp = value

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int):
        self._hp = max(0, min(value, self._max_hp))  # clamp entre 0 et max_hp

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        self._sprite = value

    @property
    def sprite_path(self) -> str:
        return self._sprite_path

    @sprite_path.setter
    def sprite_path(self, value: str):
        self._sprite_path = value
        self._sprite = pygame.image.load(value).convert_alpha()
