import pygame
import pytest

from src.page.component.dragons_panel import DragonsPanel


class MockDragon:
    """Mock minimal de Dragon pour les tests du panel"""
    def __init__(self, name="Draco", hp=50, max_hp=100):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        # sprite factice si le panel dessine quelque chose
        self.image_sprite = [pygame.Surface((64, 64))]


class TestDragonsPanel:

    @pytest.fixture(autouse=True)
    def init_pygame(self):
        pygame.init()
        pygame.font.init()
        yield
        pygame.quit()

    def test_initialization(self):
        panel = DragonsPanel(x=0, y=0, width=600, height=400)

        assert panel.width == 600
        assert panel.height == 400
        assert panel.x == 0
        assert panel.y == 0
        assert panel.cell_width > 0
        assert panel.cell_height > 0

    def test_update_cell_size(self):
        panel = DragonsPanel(x=0, y=0, width=600, height=400)

        initial_cell_width = panel.cell_width
        initial_cell_height = panel.cell_height

        panel.width = 800
        panel.height = 600
        panel._update_cell_size()

        assert panel.cell_width != initial_cell_width
        assert panel.cell_height != initial_cell_height

    def test_draw_dragon_cell(self):
        panel = DragonsPanel(x=0, y=0, width=600, height=400)
        screen = pygame.Surface((800, 600))

        dragon = MockDragon()
        cell_rect = panel._draw_dragon_cell(
            screen,
            dragon,
            x=10,
            y=10,
            is_selected=False
        )

        assert isinstance(cell_rect, pygame.Rect)
        assert cell_rect.width == panel.cell_width - 4
        assert cell_rect.height == panel.cell_height - 4
