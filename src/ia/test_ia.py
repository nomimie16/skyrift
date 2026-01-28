import pygame

import src.screen_const as sc
from src.component.entities.dragon import Dragonnet
from src.ia.ia_player import IAPlayer
from src.page.component.grid_component import GridComponent
from src.page.component.map_builder import MapBuilder
from src.player import Player
from src.page.ui import UIOverlay
from src.events.dragonEvents import DragonEvents
from src.component.entities.base import Base

# Initialiser pygame pour charger les sprites
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
ui = UIOverlay(screen)
pygame.display.set_caption("SkyRift")


running = True




# Créer joueurs
ia_player = Player(name="IA", color="bleu")
enemy_player = Player(name="Enemy", color="rouge")

grid_comp = GridComponent(
    cols=sc.COLS,
    rows=sc.ROWS,
    tile=sc.TILE_SIZE,
    origin=(sc.OFFSET_X, sc.OFFSET_Y)
)
builder = MapBuilder(grid_comp.grid, ia_player, enemy_player)
grid_comp.grid = builder.build_map()
grid = grid_comp.grid

# Créer dragons
ia_dragon = Dragonnet(5, 2, player=ia_player)
enemy_dragon_1 = Dragonnet(10, 10, player=enemy_player)

# Ajouter dragons aux joueurs
ia_player.add_unit(ia_dragon)
enemy_player.add_unit(enemy_dragon_1)

# Ajouter dragons à la grille
grid.add_occupant(ia_dragon, grid.cells[5][2])
grid.add_occupant(enemy_dragon_1, grid.cells[11][11])
grid.add_static_occupants(Base(1, 1, sprite_path="src/assets/img/base.png", player=enemy_player), grid.cells[1][1], 4, 4)
print("=== INITIAL GRID SETUP ===")
# print(grid)

dragon_events = DragonEvents(grid, origin=(sc.OFFSET_X, sc.OFFSET_Y), tile_size=sc.TILE_SIZE)


# Créer l'IA
ia = IAPlayer(player=ia_player, ennemy=enemy_player, grid=grid, dragon_events=dragon_events)

# Simuler un tour
print("=== IA TURN TEST ===")
# for dragon in ia_player.units:
#     best_cell = ia.decide_move(dragon)
#     print(f"IA dragon at ({dragon.cell.position.x},{dragon.cell.position.y}) "
#           f"wants to move to ({best_cell.position.x},{best_cell.position.y})")

turn=0
ia.play_turn(turn)



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(pygame.image.load("src/assets/img/game_background.png").convert(), (0, 0))
    grid_comp.draw(screen)
        
    for unit in ia_player.units + enemy_player.units:
        unit.draw(screen)
        unit.update()

    if all(not d.moving for d in ia_player.units):
        for d in ia_player.units:
            d.reset_actions()
        ia.play_turn(turn)
        turn += 1

    ui.draw(screen, current_player=ia_player)

    pygame.display.flip()
pygame.quit()
