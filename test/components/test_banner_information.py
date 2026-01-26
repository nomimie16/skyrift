import pygame
from src.const import FONT_BUTTON_PATH
from src.enum.event_enum import TypeEventEnum
from src.page.component.banner_information import BannerInformation

# Classe test pour BannerInformation
class TestBannerInformation:
    def test_initialization(self):
        banner = BannerInformation(None, 10, 20, 300, 40)
        assert banner.event_description is None
        assert banner.x == 10
        assert banner.y == 20
        assert banner.width == 300
        assert banner.height == 40
        assert banner.active is False

    def test_show_method(self):
        banner = BannerInformation(None)
        event_desc = TypeEventEnum.MORT_ADVERSAIRE 
        banner.show(event_desc)
        assert banner.event_description == event_desc
        assert banner.active is True
        assert banner.start_time is not None

    def test_draw_method_inactive(self):
        banner = BannerInformation(None)
        screen = pygame.Surface((800, 600))
        banner.draw(screen)  # Ne devrait rien dessiner car inactive

    def test_draw_method_active(self):
        pygame.init()
        pygame.font.init()
        banner = BannerInformation(TypeEventEnum.MORT_ADVERSAIRE)
        screen = pygame.Surface((800, 600))
        banner.show(TypeEventEnum.MORT_ADVERSAIRE)
        banner.start_time -= 2000
        banner.draw(screen)

    def test_draw_method_expired(self):
        banner = BannerInformation(TypeEventEnum.MORT_ADVERSAIRE)  
        screen = pygame.Surface((800, 600))
        banner.show(TypeEventEnum.MORT_ADVERSAIRE)  
        banner.start_time -= 5000  # Simuler que la bannière a été affichée il y a 5 secondes
        banner.draw(screen)  # Devrait désactiver la bannière
        assert banner.active is False
    