import pygame
import pytest

from src.page.component.grid_component import GridComponent


class TestGridComponent:

    @pytest.fixture(autouse=True)
    def init_pygame(self):
        pygame.init()
        yield
        pygame.quit()

    def test_initialization(self):
        grid_component = GridComponent(cols=5, rows=4, tile=32, origin=(10, 20))

        assert grid_component.grid.nb_columns == 5
        assert grid_component.grid.nb_rows == 4
        assert grid_component.tile == 32
        assert grid_component.origin == (10, 20)

    def test_draw_method(self):
        screen = pygame.Surface((200, 200))
        grid_component = GridComponent(cols=3, rows=3, tile=50, origin=(0, 0))

        # Le test passe s'il n'y a pas d'exception
        grid_component.draw(screen)

    def test_handle_click_inside(self):
        grid_component = GridComponent(cols=4, rows=4, tile=40, origin=(0, 0))

        cell = grid_component.handle_click((70, 90))

        assert cell is not None
        assert cell.position.x == 1  # colonne
        assert cell.position.y == 2  # ligne

    def test_handle_click_outside(self):
        grid_component = GridComponent(cols=4, rows=4, tile=40, origin=(0, 0))

        cell = grid_component.handle_click((200, 200))

        assert cell is None

    def test_handle_click_with_offset(self):
        grid_component = GridComponent(cols=4, rows=4, tile=40, origin=(10, 10))

        cell = grid_component.handle_click((50, 70))

        assert cell is not None
        assert cell.position.x == 1
        assert cell.position.y == 1
