from typing import List

import pygame

import screen_const as sc
from component.enum.type_entities import TypeEntitiesEnum
from component.grid import Cell
from component.position import Position
from player import Player
from screen_const import TILE_SIZE


class Entity:
    """Classe de base pour toutes les entités du jeu"""

    def __init__(self, x: int, y: int, name: str, type_entity: List[TypeEntitiesEnum], max_hp: int, attack_damage: int,
                 attack_range: int, sprite_path: str, kill_reward: int = 0):
        self._cell: Cell = Cell(x, y)
        self._pixel_pos = self.cell.get_pixel_position()
        self._name: str = name
        self._type_entity: List[TypeEntitiesEnum] = type_entity
        self._max_hp: int = max_hp
        self._hp: int = max_hp
        self._attack_damage: int = attack_damage
        self._attack_range: int = attack_range
        self._sprite_path: str = sprite_path
        self._sprite = pygame.image.load(sprite_path).convert_alpha()
        self._kill_reward = kill_reward
        self._last_attacker: Player | None = None

    def draw(self, surface) -> None:
        """
        Affichage d'une entité
        :param surface: Surface sur laquelle l'entité est placée
        :return: None
        """
        surface.blit(self._sprite, self._cell.get_pixel_position().to_tuple())

    def draw_health_bar(self, surface, width=1, gap=0) -> None:
        """
        Dessine la barre de vie de l'entité
        :param: surface: Surface sur laquelle dessiner la barre de vie
        :return: None
        """
        if self._hp <= 0:
            return

        BAR_WIDTH = sc.TILE_SIZE * width
        BAR_HEIGHT = 6
        OFFSET_Y = -10

        x = self._pixel_pos.x
        y = self._pixel_pos.y + OFFSET_Y - gap * TILE_SIZE

        hp_ratio = self._hp / self._max_hp
        current_width = int(BAR_WIDTH * hp_ratio)

        if hp_ratio > 0.6:
            color = (0, 200, 0)  # Vert
        elif hp_ratio > 0.3:
            color = (255, 165, 0)  # Orange
        else:
            color = (200, 0, 0)  # Rouge

        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (x, y, BAR_WIDTH, BAR_HEIGHT)
        )

        pygame.draw.rect(
            surface,
            color,
            (x, y, current_width, BAR_HEIGHT)
        )

    def take_damage(self, amount) -> None:
        """
        Inflige des dégâts à l'entité
        :param: amount: montant des dégâts
        :return: None
        """
        self._hp = max(0, self._hp - amount)

    def heal(self, amount) -> None:
        if self._hp <= 0:
            return
        self._hp = min(self._hp + amount, self._max_hp)

    def is_dead(self) -> bool:
        """
        Vérifie si l'entité est morte
        :return: boolean
        """
        return self._hp <= 0

    def attack(self, target) -> None:
        """
        attaque la cible choisie
        :param: target : l'entité ciblée
        :return: None
        """
        target.take_damage(self.attack_damage)

    def grant_rewards(self) -> None:
        """
        Accorde les récompenses à l'attaquant
        :return:
        """
        if self._last_attacker and self.kill_reward > 0:
            self._last_attacker.economy.earn_gold(self.kill_reward)

    # ------- Getters et Setters -------

    @property
    def cell(self) -> Cell:
        return self._cell

    @cell.setter
    def cell(self, value: Cell) -> None:
        self._cell = value

    @property
    def pixel_pos(self) -> Position:
        return self._pixel_pos

    @pixel_pos.setter
    def pixel_pos(self, value) -> None:
        self._pixel_pos = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def type_entity(self) -> list[TypeEntitiesEnum]:
        return self._type_entity

    @type_entity.setter
    def type_entity(self, value: List[TypeEntitiesEnum]) -> None:
        self._type_entity = value

    @property
    def max_hp(self) -> int:
        return self._max_hp

    @max_hp.setter
    def max_hp(self, value: int) -> None:
        self._max_hp = value

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self._max_hp))

    @property
    def attack_damage(self) -> int:
        return self._attack_damage

    @attack_damage.setter
    def attack_damage(self, value: int) -> None:
        self._attack_damage = value

    @property
    def attack_range(self) -> int:
        return self._attack_range

    @attack_range.setter
    def attack_range(self, value: int) -> None:
        self._attack_range = value

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value) -> None:
        self._sprite = value

    @property
    def sprite_path(self) -> str:
        return self._sprite_path

    @sprite_path.setter
    def sprite_path(self, value: str) -> None:
        self._sprite_path = value
        self._sprite = pygame.image.load(value).convert_alpha()

    @property
    def last_attacker(self) -> Player | None:
        return self._last_attacker

    @last_attacker.setter
    def last_attacker(self, value: Player) -> None:
        self._last_attacker = value

    @property
    def kill_reward(self) -> int | None:
        return self._kill_reward
