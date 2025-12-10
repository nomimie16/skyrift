import pygame
import sys
from page.main import taille_ecran, screen


pygame.init()

TILE_SIZE = 40 #taille tuile en pixels
screen_w , screen_h = screen.get_size()
rows = screen_h // TILE_SIZE
cols = screen_w // TILE_SIZE

grid_w = cols * TILE_SIZE
grid_h = rows * TILE_SIZE
offset_x = (screen_w - grid_w) // 2
offset_y = (screen_h - grid_h) // 2

pygame.display.set_caption("Dragon Grid Movement")
clock = pygame.time.Clock()

# chargement du fond
background = pygame.image.load("assets/img/backgroundsquare.png").convert_alpha()
background = pygame.transform.scale(background, screen.get_size())

# grille pour la map
# 0 vide (pas de plateforme)
# 1  plateforme (sur laquelle le dragon peut marcher)
# Creation des platformes de la map
MAP = [[1 for _ in range(cols)] for _ in range(rows)]



#placement dragon(carré rouge)
dragon_pos = [0,0]  
DRAGON_COLOR = (255,50,50)

def draw_map():
    """ dessine la map en fonction de la grille choisie"""
    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(offset_x + c*TILE_SIZE, offset_y + r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
           
            # Optional: draw grid
            pygame.draw.rect(screen, (150,150,150), rect, 1)

def get_clicked_tile(mouse_pos):
    x, y = mouse_pos
    x -= offset_x
    y -= offset_y
    col = x // TILE_SIZE
    row = y // TILE_SIZE
    if 0 <= col < cols and 0 <= row < rows:
        return (row, col)
    return None 

def is_adjacent(dragon, target):
    dr, dc = dragon
    tr, tc = target
    # uniquement cases adjacentes 
    return abs(dr - tr) + abs(dc - tc) == 1

def can_move_to(tile):
    r, c = tile
    if 0 <= r < rows and 0 <= c < cols:
        return MAP[r][c] == 1
    return False

# boucle
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = get_clicked_tile(pygame.mouse.get_pos())
            if clicked and is_adjacent(dragon_pos, clicked) and can_move_to(clicked):
                dragon_pos = list(clicked)


    screen.blit(background, (0,0))  # fond 
    draw_map()

    # dessiner dragon
    dr, dc = dragon_pos
    dragon_rect = pygame.Rect(offset_x +dc*TILE_SIZE, offset_y +dr*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, DRAGON_COLOR, dragon_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
