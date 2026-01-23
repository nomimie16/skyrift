import math

import pygame

import src.screen_const as sc


class Fireball:
    """Boule de feu qui se déplace d'une entité de départ à une entité cible"""

    def __init__(self, start_entity, target_entity):

        direction_gauche = False
        if hasattr(start_entity, 'sprite_path') and "gauche" in start_entity.sprite_path:
            self.start_x = start_entity.pixel_pos.x
        elif hasattr(start_entity, 'sprite_path') and "droite" in start_entity.sprite_path:
            self.start_x = start_entity.pixel_pos.x + sc.TILE_SIZE
        else:
            self.start_x = start_entity.pixel_pos.x + sc.TILE_SIZE // 2

        if direction_gauche:
            self.start_x = start_entity.pixel_pos.x
        else:
            self.start_x = start_entity.pixel_pos.x + sc.TILE_SIZE

        self.start_y = start_entity.pixel_pos.y + sc.TILE_SIZE // 2

        self.target_x = target_entity.pixel_pos.x + sc.TILE_SIZE // 2
        self.target_y = target_entity.pixel_pos.y + sc.TILE_SIZE // 2

        self.x = self.start_x
        self.y = self.start_y

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        self.distance = math.sqrt(dx ** 2 + dy ** 2)

        self.duration = 500

        self.start_time = pygame.time.get_ticks()
        self.active = True
        self.sprite_path = pygame.image.load("src/assets/sprites/boule_de_feu.png").convert_alpha()
        self.active = True

        angle = math.degrees(math.atan2(-dy, dx))
        self.sprite = pygame.transform.rotate(self.sprite_path, angle)

    def update(self):
        """Met à jour la position de la boule de feu"""
        if not self.active:
            return False

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        progress = elapsed_time / self.duration

        if progress >= 1:
            self.x = self.target_x
            self.y = self.target_y
            self.active = False
            return False

        self.x = self.start_x + (self.target_x - self.start_x) * progress
        self.y = self.start_y + (self.target_y - self.start_y) * progress
        return True

    def draw(self, screen):
        """
        Dessine la boule de feu à l'écran
        :param screen:
        :return:
        """
        if self.active:
            rect = self.sprite.get_rect(center=(self.x, self.y))
            screen.blit(self.sprite, rect)
