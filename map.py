import pygame

from page.main import screen

file = 'assets/img/map.png'


class Game:

    def __init__(self):
        pygame.init()
        self.screen = screen
        pygame.display.set_caption("Pygame Tiled Demo")
        self.running = True

    def run(self):
        self.load_image(file)

        pygame.quit()

    def load_image(self, file):
        self.file = file
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()

        self.screen = pygame.display.set_mode(self.rect.size)
        pygame.display.set_caption(f'size:{self.rect.size}')
        self.screen.blit(self.image, self.rect)
        pygame.display.update()

    # def draw_map(rows, cols, offset_x, offset_y, TILE_SIZE):
    #     """ dessine la map en fonction de la grille choisie"""
    #     for r in range(rows):
    #         for c in range(cols):
    #             rect = pygame.Rect(offset_x + c * TILE_SIZE, offset_y + r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    #
    #             # Optional: draw grid
    #             pygame.draw.rect(screen, (150, 150, 150), rect, 1)


game = Game()
game.run()
