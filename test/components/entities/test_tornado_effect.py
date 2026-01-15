from src.component.entities.effect_zone import EffectZone
from src.component.entities.entity import Entity

# Classe de test pour TornadoEffect
class TestTornadoEffect(EffectZone):
    def __init__(self, damage: int = 2, speed_penalty: int = -2):
        self.damage = damage
        self.speed_penalty = speed_penalty
    def test_apply_effect(self, mock_entity: Entity):
        """Test de l'application de l'effet de tornade sur une entité."""
        initial_hp = mock_entity.hp
        initial_speed = mock_entity.actual_speed

        self.apply_effect(mock_entity)

        assert mock_entity.hp == initial_hp - self.damage
        assert mock_entity.speed_modifier == self.speed_penalty
        assert mock_entity.actual_speed == max(0, mock_entity.speed_base + self.speed_penalty)
    def test_remove_effect(self, mock_entity: Entity):
        """Test du retrait de l'effet de tornade sur une entité."""
        self.apply_effect(mock_entity)
        self.remove_effect(mock_entity)

        assert mock_entity.speed_modifier == 0
        assert mock_entity.actual_speed == mock_entity.speed_base
    