import pygame

from src.component.grid import Grid


class GridComponent:
    def __init__(self, cols, rows, tile, origin=(0, 0)):
        self.grid = Grid(cols, rows)
        self.origin = origin
        self.tile = tile

    def draw(self, screen):
        """dessine la grille sur l'écran"""
        ox, oy = self.origin
        for r in range(self.grid.nb_rows):
            for c in range(self.grid.nb_columns):
                rect = pygame.Rect(
                    ox + c * self.tile,
                    oy + r * self.tile,
                    self.tile,
                    self.tile
                )
                pygame.draw.rect(screen, (220, 220, 220), rect, 1)

    def handle_click(self, pos):
        """renvoie la case cliquée"""
        x, y = pos
        ox, oy = self.origin

        # clique hors de la zone
        if not (ox <= x < ox + self.grid.nb_columns * self.tile and
                oy <= y < oy + self.grid.nb_rows * self.tile):
            return None

        grid_x = (x - ox) // self.tile
        grid_y = (y - oy) // self.tile
        return self.grid.cells[grid_y][grid_x]
