from random import randint

from component.entities.entity import Entity
from component.entities.static_entity import StaticEntity


class Tornado(StaticEntity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, name="Tornade", sprite_path="assets/sprites/tornado.png", width=128, height=128)
        self._duration = randint(1, 5)  # nombre de tours restants avant disparition

    def apply_effect(self, entity: Entity):
        """
        Ajoute un effet de perte de vitesse au dragon
        :param entity:
        :return:
        """
        if self.rect.collidepoint(entity.position.x, entity.position.y):
            entity.speed_modifier = -2
            entity.movement_points = max(0, entity.base_speed + entity.speed_modifier)

    def update(self):
        """Appeler à chaque tour : diminue la durée de vie de la tornade."""
        self.duration -= 1
        return self.duration > 0
