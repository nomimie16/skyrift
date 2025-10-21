from unittest.mock import patch, Mock
from component.entities.volcano import Volcano
from component.entities.dragon import DragonMoyen

# simule les surfaces
def _surface_mock(collide=True):
    surface = Mock()
    rect = Mock()
    rect.collidepoint.return_value = collide
    surface.get_rect.return_value = rect
    return surface

class TestVolcano:

    def setup_method(self):
        # patch là où EffectZone importe/appele pygame.image.load
        with patch("component.entities.effect_zone.pygame.image.load") as mock_load:
            mock_load.return_value = _surface_mock(collide=True)
            self.volcano = Volcano(1, 1, sprite_path="test.png")
            self.dragon = DragonMoyen(1, 1)

    def test_life_loss(self):
        self.volcano.apply_effect(self.dragon)
        assert self.dragon.hp == 118

    def test_speed_loss(self):
        self.volcano.apply_effect(self.dragon)
        assert self.dragon._speed_modifier == 0