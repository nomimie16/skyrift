from component.entities.effect_zone import EffectZone


class PurseEffect(EffectZone):
    """
    Effet de volcan : brûle et ralentit le dragon.
    """

    def __init__(self, gold: int = 50):
        self.gold = gold
