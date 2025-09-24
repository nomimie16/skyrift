import pygame

from component.position import Position


class Entity:
    def __init__(self, x, y, max_hp, sprite_path):
        self.position = Position(x, y)
        self.max_hp = max_hp
        self.hp = max_hp
        self.sprite = pygame.image.load(sprite_path).convert_alpha()

    def draw(self, surface):
        surface.blit(self.sprite, (self.position.x, self.position.y))

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def is_dead(self):
        return self.hp <= 0
