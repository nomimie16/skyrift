import pygame
import pytest
from src.const import FONT_BUTTON_PATH
from src.page.component.gold_popup import GoldPopup, GoldPopupManager

@pytest.fixture(autouse=True)
def init_pygame():
    """Initialise pygame et le module font pour les tests"""
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()
    
# Classe test pour GoldPopup et GoldPopupManager
class TestGoldPopup:
    def test_initialization_gain(self):
        popup = GoldPopup(100, 200, 50)
        assert popup.amount == 50
        assert popup.x == 100
        assert popup.y == 200
        assert popup.color == (50, 200, 50)  # Vert pour le gain
        assert popup.text == "+50"
        assert popup.alive is True

    def test_initialization_loss(self):
        popup = GoldPopup(150, 250, -30)
        assert popup.amount == -30
        assert popup.x == 150
        assert popup.y == 250
        assert popup.color == (220, 50, 50)  # Rouge pour la perte
        assert popup.text == "-30"
        assert popup.alive is True

    def test_update_method(self):
        popup = GoldPopup(100, 200, 20, duration=500)
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
        popup = GoldPopup(100, 200, 15)
        screen = pygame.Surface((800, 600))
        popup.draw(screen)  # Devrait dessiner le texte sans erreur
    
# Classe test pour GoldPopupManager
class TestGoldPopupManager:
    def test_spawn(self):
        manager = GoldPopupManager()
        manager.spawn(200, 300, 40)
        assert len(manager.popups) == 1
        popup = manager.popups[0]
        assert popup.x == 200
        assert popup.y == 300
        assert popup.amount == 40
        manager.spawn(250, 350, -20)
        assert len(manager.popups) == 2 
        popup_loss = manager.popups[1]
        assert popup_loss.amount == -20 
        assert popup_loss.color == (220, 50, 50)  # Rouge pour la perte
        assert popup_loss.text == "-20"
        assert popup_loss.x == 250
        assert popup_loss.y == 350
    