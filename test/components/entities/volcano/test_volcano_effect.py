import pytest
from src.player import Player
from src.component.entities.dragon import Dragonnet
from src.component.entities.volcano.volcano_effect import VolcanoEffect

class TestVolcanoEffect:

    def test_apply_effect_deals_damage(self):
        player = Player("Test Player", "bleu")
        dragon = Dragonnet(12, 12, player)
        initial_hp = dragon.hp
        effect = VolcanoEffect(damage=5)

        effect.apply_effect(dragon)

        assert dragon.hp == initial_hp - 5

    def test_apply_effect_applies_speed_penalty(self):
        player = Player("Test Player", "bleu")
        dragon = Dragonnet(20, 12, player)
        base_speed = dragon.speed_base
        effect = VolcanoEffect(damage=0, speed_penalty=-1)

        effect.apply_effect(dragon)

        assert dragon.speed_modifier == -1
        assert dragon.actual_speed == base_speed - 1

    def test_speed_never_goes_below_zero(self):
        player = Player("Test Player", "bleu")
        dragon = Dragonnet(20, 20, player)
        effect = VolcanoEffect(damage=0, speed_penalty=-100)

        effect.apply_effect(dragon)

        assert dragon.actual_speed == 0

    def test_remove_effect_resets_speed(self):
        player = Player("Test Player", "bleu")
        dragon = Dragonnet(10, 10, player)
        effect = VolcanoEffect(speed_penalty=-2)

        effect.apply_effect(dragon)
        effect.remove_effect(dragon)

        assert dragon.speed_modifier == 0
        assert dragon.actual_speed == dragon.speed_base
        
    def test_damage_only_does_not_change_speed(self):
        player = Player("Test Player", "bleu")
        dragon = Dragonnet(10, 10, player)
        base_speed = dragon.actual_speed
        effect = VolcanoEffect(damage=5, speed_penalty=0)

        effect.apply_effect(dragon)

        assert dragon.actual_speed == base_speed

