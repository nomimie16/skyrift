from component.entities.effect_zone import EffectZone
from player import Player


class PurseEffect(EffectZone):
    """
    Effet de volcan : brûle et ralentit le dragon.
    """

    def __init__(self, gold: int = 50):
        self.gold = gold

    def apply_effect(self, player: Player):
        player.economy.earn_gold(self.gold)
        print(("player gold after purse effect:", player.economy.get_gold()))
