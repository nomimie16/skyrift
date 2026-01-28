import random

import pygame

from src import screen_const as sc
from src.component.entities.purse_effect import PurseEffect
from src.component.entities.zone_entity import ZoneEntity
from src.component.grid import Grid
from src.component.sound import sound
from src.const import PURSE_SPAWN_CHANCE_PER_TURN
from src.enum.type_entities import TypeEntitiesEnum


def spawn_random_purse(grid: Grid, amount: int = 50) -> 'Purse | None':
    """
    Fait spawn une bourse avec une probabilité donnée
    """

    if Purse.instances_count >= 5:
        return None

    if random.random() > PURSE_SPAWN_CHANCE_PER_TURN:
        return None

    free_cells = grid.free_cells()
    if not free_cells:
        return None

    cell = random.choice(free_cells)
    purse = Purse(cell.position.x, cell.position.y, amount)
    grid.add_occupant(purse, cell)
    sound.play("magic.wav")  # apparition de bourse

    return purse


class Purse(ZoneEntity):
    """
    Bourse d'or que le joueur peut ramasser
    50 pièces d'or par défaut
    """

    instances_count = 0

    def __init__(self, x_cell: int, y_cell: int, amount: int = 50):
        super().__init__(x_cell, y_cell,
                         sprite_path="src/assets/sprites/purse.png", width=1, height=1,
                         type_entity=[TypeEntitiesEnum.EFFECT_ZONE, TypeEntitiesEnum.PLAYER_EFFECT_ZONE],
                         zone_effect=PurseEffect())
        self.name = "Bourse"
        self._amount: int = amount

        self.start_time = pygame.time.get_ticks()
        self.duration = 1000

        self._target_y = self.pixel_pos.y
        self.start_y = self._target_y - 200

        self._pixel_pos.y = self.start_y
        self.is_falling = True

        self._current_opacity = 0

        Purse.instances_count += 1

    def update(self):
        """Met à jour l'animation de la bourse en fonction du temps
        https://easings.net/#easeOutCubic
        """
        if not self.is_falling:
            return

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time

        progress = min(elapsed / self.duration, 1.0)

        ease = 1 - pow(1 - progress, 3)

        self._pixel_pos.y = self.start_y + (self.target_y - self.start_y) * ease

        self._current_opacity = int(255 * progress)

        if progress >= 1.0:
            self._pixel_pos.y = self.target_y
            self._current_opacity = 255
            self.is_falling = False

    def destroy(self) -> None:
        """
        Détruit l'instance de la bourse
        :return: None
        """
        Purse.instances_count -= 1

    def draw(self, surface) -> None:
        """
        Dessine la bourse à l'écran
        :param surface: Surface sur laquelle dessiner la bourse
        :return: None
        """
        scaled_width = int(self.width * sc.TILE_SIZE * 2)
        scaled_height = int(self.height * sc.TILE_SIZE * 2)
        if not self.is_falling:
            scaled_sprite = pygame.transform.scale(self._sprite, (scaled_width, scaled_height))
        else:
            scaled_sprite = pygame.transform.scale(self._sprite, (scaled_width, scaled_height))
            scaled_sprite.set_alpha(self._current_opacity
                                    )
        x = self._pixel_pos.x - (scaled_width - sc.TILE_SIZE) // 2
        y = self._pixel_pos.y - (scaled_height - sc.TILE_SIZE)

        surface.blit(scaled_sprite, (x, y))

    # ------- Getters et Setters -------

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, value: int) -> None:
        self._amount = value

    @property
    def target_y(self) -> int:
        return self._target_y
