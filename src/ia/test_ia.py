import pygame

import src.screen_const as sc
from src.component.entities.dragon import Dragonnet
from src.ia.ia_player import IAPlayer
from src.page.component.grid_component import GridComponent
from src.page.component.map_builder import MapBuilder
from src.player import Player

# Initialiser pygame pour charger les sprites
pygame.init()

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
enemy_dragon_1 = Dragonnet(22, 15, player=enemy_player)

# Ajouter dragons aux joueurs
ia_player.add_unit(ia_dragon)
enemy_player.add_unit(enemy_dragon_1)

# Ajouter dragons à la grille
grid.add_occupant(ia_dragon, grid.cells[6][6])
grid.add_occupant(enemy_dragon_1, grid.cells[11][11])
print("=== INITIAL GRID SETUP ===")
print(grid)

# Créer l'IA
ia = IAPlayer(player=ia_player, ennemy=enemy_player, grid=grid)

# Simuler un tour
print("=== IA TURN TEST ===")
for dragon in ia_player.units:
    best_cell = ia.decide_move(dragon)
    print(f"IA dragon at ({dragon.cell.position.x},{dragon.cell.position.y}) "
          f"wants to move to ({best_cell.position.x},{best_cell.position.y})")
