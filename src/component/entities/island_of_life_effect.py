from src.component.entities.effect_zone import EffectZone
from src.component.entities.entity import Entity


class IslandOfLifeEffect(EffectZone):
    """
    Effet de l'île de vie : soigne les entités qui y entrent.
    """

    def __init__(self, hp: int = 7):
        self.heal = hp

    def apply_effect(self, entity: Entity) -> int:
        """Applique l'effet de l'île de vie à l'entité donnée.
        :param: entity (Entity): L'entité à affecter.
        :return: None
        """
        if entity.hp < entity.max_hp:
            entity.heal(self.heal)
            return self.heal
        return 0
