from typing import List

import pygame

from component.enum.type_entities import TypeEntitiesEnum
from component.grid import Grid
from component.position import Position


class Entity:
    def __init__(self, x: int, y: int, name: str, type_entity: List[TypeEntitiesEnum], max_hp: int, attack_damage: int,
                 attack_range: int, sprite_path: str):
        self._position: Position = Position(x, y)
        self._name: str = name
        self._type_entity: List[TypeEntitiesEnum] = type_entity
        self._max_hp: int = max_hp
        self._hp: int = max_hp
        self._attack_damage: int = attack_damage
        self._attack_range: int = attack_range
        self._sprite_path: str = sprite_path
        self._sprite = pygame.image.load(sprite_path).convert_alpha()

    def draw(self, surface):
        """
        Affichage d'une entité
        @:param surface: Surface sur laquelle l'entité est placée
        """
        surface.blit(self._sprite, (self._position.x, self._position.y))

    def take_damage(self, amount):
        """
        Inflige des dégâts à l'entité
        @:param amount:
        """
        self._hp = max(0, self._hp - amount)

    def is_dead(self):
        """
        Vérifie si l'entité est morte
        :return: boolean
        """
        return self._hp <= 0

    def attack(self, target, amount):
        """
        attaque la cible choisie
        @param target : l'entité ciblée
        @param amount : le nombre de degats a infliger
        """
        target.take_damage(amount)

    def attack(self, target_entity):
        """
        Attaque une autre entité en lui infligeant des dégâts
        @:param target_entity: Entité cible de l'attaque
        @:param damage: Montant des dégâts infligés
        """
        print("distance :", Grid.distance(self, target_entity), "range:", self._attack_range)
        if Grid.distance(self, target_entity) <= self._attack_range:
            target_entity.take_damage(self._attack_damage)

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
    def type_entity(self) -> list[TypeEntitiesEnum]:
        return self._type_entity

    @type_entity.setter
    def type_entity(self, value: List[TypeEntitiesEnum]):
        self._type_entity = value

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

    # ------- Getters et Setters -------

    @property
    def attack_damage(self) -> int:
        return self._attack_damage

    @attack_damage.setter
    def attack_damage(self, value: int):
        self._attack_damage = value

    @property
    def attack_range(self) -> int:
        return self._attack_range

    @attack_range.setter
    def attack_range(self, value: int):
        self._attack_range = value

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
