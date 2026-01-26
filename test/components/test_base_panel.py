import pygame
import pytest
from src.page.component.base_panel import BasePanel


@pytest.fixture(autouse=True)
def init_pygame():
    """Initialise pygame et le module font pour les tests"""
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()


class TestBasePanel:

    def test_initialization(self):
        panel = BasePanel(width=300, x=10, y=20, height=200)

        assert panel.width == 300
        assert panel.height == 200
        assert panel.x == 10
        assert panel.y == 20

        assert panel.font_title is not None
        assert panel.font_normal is not None
        assert panel.font_small is not None
        assert panel.font_tiny is not None

    def test_set_position(self):
        panel = BasePanel(300, 0, 0, 200)
        panel.set_position(50, 80)

        assert panel.x == 50
        assert panel.y == 80

    def test_get_hp_color(self):
        panel = BasePanel(300, 0, 0, 200)

        assert panel._get_hp_color(80, 100) == panel.HP_COLOR_HIGH
        assert panel._get_hp_color(40, 100) == panel.HP_COLOR_MEDIUM
        assert panel._get_hp_color(10, 100) == panel.HP_COLOR_LOW
        assert panel._get_hp_color(0, 0) == panel.HP_COLOR_LOW

    def test_draw_wood_frame(self):
        panel = BasePanel(300, 10, 10, 200)
        surface = pygame.Surface((800, 600))

        # Ne doit pas lever d'exception
        panel._draw_wood_frame(surface)

    def test_draw_separator(self):
        panel = BasePanel(300, 10, 10, 200)
        surface = pygame.Surface((800, 600))

        panel._draw_separator(surface, y=100)

    def test_draw_hp_bar(self):
        panel = BasePanel(300, 10, 10, 200)
        surface = pygame.Surface((800, 600))

        color = panel._draw_hp_bar(
            surface=surface,
            x=50,
            y=50,
            width=200,
            height=20,
            current_hp=50,
            max_hp=100
        )

        assert color in (
            panel.HP_COLOR_HIGH,
            panel.HP_COLOR_MEDIUM,
            panel.HP_COLOR_LOW
        )
