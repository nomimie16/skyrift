import pygame
import pytest
from src.const import FONT_BUTTON_PATH
from src.page.component.damage_heal_popup import DamageAndHealPopup, DamageAndHealPopupManager

@pytest.fixture(autouse=True)
def init_pygame():
    """Initialise pygame et le module font pour les tests"""
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()
    
# Classe test pour DamageAndHealPopup et DamageAndHealPopupManager
class TestDamageAndHealPopup:
    def test_initialization_damage(self):
        popup = DamageAndHealPopup(100, 200, -50)
        assert popup.amount == -50
        assert popup.x == 100
        assert popup.y == 200
        assert popup.color == (220, 50, 50)  # Rouge pour les dégâts
        assert popup.text == "-50"
        assert popup.alive is True

    def test_initialization_heal(self):
        popup = DamageAndHealPopup(150, 250, 30)
        assert popup.amount == 30
        assert popup.x == 150
        assert popup.y == 250
        assert popup.color == (50, 200, 50)  # Vert pour les soins
        assert popup.text == "+30"
        assert popup.alive is True

    def test_update_method(self):
        popup = DamageAndHealPopup(100, 200, -20, duration=500)
        initial_y = popup.y
        pygame.time.delay(300)  # Attendre 300 ms
        popup.update()
        assert popup.y < initial_y  # Le texte doit monter
        assert popup.alive is True
        pygame.time.delay(300)  # Attendre encore 300 ms
        popup.update()
        assert popup.alive is False  # Le texte doit être mort après la durée

    def test_draw_method(self):
        pygame.init()
        pygame.font.init()
        popup = DamageAndHealPopup(100, 200, -15)
        screen = pygame.Surface((800, 600))
        popup.draw(screen)  # Devrait dessiner le texte sans erreur
    
    

# Classe test pour DamageAndHealPopupManager
class TestDamageAndHealPopupManager:
    def test_spawn_for_entity(self):
        class MockEntity:
            def __init__(self, x, y):
                self.pixel_pos = pygame.math.Vector2(x, y)

        manager = DamageAndHealPopupManager()
        entity = MockEntity(50, 100)
        manager.spawn_for_entity(entity, -25)
        assert len(manager.popups) == 1
        popup = manager.popups[0]
        assert popup.x == 82  # 50 + 32
        assert popup.y == 90  # 100 - 10
        assert popup.amount == -25
        manager.spawn_for_entity(entity, 40)
        assert len(manager.popups) == 2
        popup_heal = manager.popups[1]
        assert popup_heal.amount == 40
        assert popup_heal.color == (50, 200, 50)  # Vert pour les soins
        assert popup_heal.text == "+40"
        assert popup_heal.x == 82  # 50 + 32
        assert popup_heal.y == 90  # 100 - 10
        assert popup_heal.amount == 40
        