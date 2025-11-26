import pygame
import sys
from page.main import taille_ecran, screen
from component.grid import Grid, Position
from component.entities.dragon import Dragonnet, Dragon, DragonMoyen


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

grid = Grid(cols, rows)

dragon = DragonMoyen(0,0)  

start_pos = dragon.position
grid.add_occupant(dragon, start_pos)

# grille pour la map
# 0 vide (peut pas marcher)
# 1  plateforme (peut marcher)
MAP = [[1 for _ in range(cols)] for _ in range(rows)]



#placement dragon(carré rouge)
dragon_pos = [0,0]  
dragon.position.x = dragon_pos[1] * TILE_SIZE
dragon.position.y = dragon_pos[0] * TILE_SIZE
DRAGON_COLOR = (255,50,50)
sprite_path = dragon.sprite_path
sprite = image = pygame.image.load(sprite_path).convert()

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
    dr, dc = dragon.position.y, dragon.position.x
    tr, tc = target
    return (dr == tr) or (dc == tc) or (abs(dr - tr) + abs(dc - tc) == 1)

def can_move_to(tile, dragon):
    distance_max = dragon._actual_speed
    print("dragon speed:", distance_max)
    r, c = tile
    # vérifie les cotés
    if not (0 <= r < rows and 0 <= c < cols):
        return False

    # vérifie que la tuile est praticable
    if MAP[r][c] != 1:
        return False

    # calcule distance de Manhattan entre dragon et la cible
    dr = dragon.position.y
    dc = dragon.position.x
    manhattan = abs(dr - r) + abs(dc - c)
    print("manhattan distance:", manhattan)
    return manhattan <= distance_max

# boucle
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = get_clicked_tile(pygame.mouse.get_pos())
            print("can move",can_move_to(clicked, dragon))
            print("adja",is_adjacent(dragon, clicked))
            print("Clicked tile:", clicked)
            print("dragon pos:", dragon.position.x, dragon.position.y)
            
            if clicked and is_adjacent(dragon, clicked) and can_move_to(clicked, dragon):
                # dragon_pos = list(clicked)
                r, c = clicked
                dragon_pos = [r, c]
                dragon.position.x = c * TILE_SIZE
                dragon.position.y = r * TILE_SIZE
                


    screen.blit(background, (0,0))  # fond 
    draw_map()

    # dessiner dragon
    dr, dc = dragon_pos
    dragon_rect = pygame.Rect(offset_x +dc*TILE_SIZE, offset_y +dr*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, DRAGON_COLOR, dragon_rect)
    print("dragon grid pos:", dc, dr)
    print("dragon pos", dragon.position.x, dragon.position.y)
    # print("dragon pixel pos:", offset_x +dc*TILE_SIZE, offset_y +dr*TILE_SIZE)
    dragon.move_dragon(offset_x +dc*TILE_SIZE, offset_y +dr*TILE_SIZE)
    dragon.update()
    # dragon.update_direction("droite")
    dragon.draw(screen)
    

    pygame.display.flip()

pygame.quit()
sys.exit()
