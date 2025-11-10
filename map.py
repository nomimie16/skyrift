import pygame
from pygame.locals import *
from page.main import screen

file = 'assets/img/map.png'

class Game:
    W = 640
    H = 1000
    SIZE = W, H

    def __init__(self):
        pygame.init()
        self.screen = screen
        pygame.display.set_caption("Pygame Tiled Demo")
        self.running = True

    def run(self):
        while self.running:
            
                
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

game = Game()
game.run()