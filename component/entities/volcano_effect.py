from component.entities.effect_zone import EffectZone
from component.entities.entity import Entity


class VolcanoEffect(EffectZone):
    """
    Effet de volcan : brûle et ralentit le dragon.
    """

    def __init__(self, damage: int = 2, speed_penalty: int = -1):
        self.damage = damage
        self.speed_penalty = speed_penalty

    def apply_effect(self, entity: Entity):
        entity.hp -= self.damage
        entity.speed_modifier = self.speed_penalty
        entity.actual_speed = max(0, entity.speed_base + entity.speed_modifier)

    def remove_effect(self, entity: Entity):
        entity.reset_speed()
