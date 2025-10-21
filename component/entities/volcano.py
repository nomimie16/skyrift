from component.entities.entity import Entity
from component.entities.effect_zone import EffectZone


class Volcano(EffectZone):
    def __init__(self, x: int, y: int, sprite_path="assets/sprites/volcano.png"):
        super().__init__(x, y, name="Volcan", sprite_path=sprite_path, width=128, height=128)

    def apply_effect(self, entity: Entity):
        """
        Ajoute un effet de perte de vitesse et de vie au dragon
        :param entity:
        :return:
        """
        if self.rect.collidepoint(entity.position.x, entity.position.y):
            entity.hp -= 2
            entity.speed_modifier = -1
            entity.movement_points = max(0, entity.base_speed + entity.speed_modifier)
        else:
            entity.reset_speed()
