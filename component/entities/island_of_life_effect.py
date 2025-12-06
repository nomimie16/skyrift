from component.entities.effect_zone import EffectZone
from component.entities.entity import Entity


class IslandOfLifeEffect(EffectZone):
    """
    Effet de volcan : brûle et ralentit le dragon.
    """

    def __init__(self, hp: int = 2):
        self.hp = hp

    def apply_effect(self, entity: Entity):
        entity.hp += 2
        print(("entity hp after island of life effect:", entity.hp))
