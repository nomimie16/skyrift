import tkinter as tk

import pygame

# Calcul des constantes de la grille

_root = tk.Tk()
_root.withdraw()
_taille_ecran = _root.winfo_screenheight()
_root.destroy()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_W, SCREEN_H = screen.get_size()

ROWS = 24
COLS = 24

PANEL_WIDTH = max(250, int(SCREEN_W * 0.15))

TOP_PCT = 0.10
BOTTOM_PCT = 0.03
LEFT_PCT = 0.10
RIGHT_PCT = 0.10

MARGIN_TOP = int(SCREEN_H * TOP_PCT)
MARGIN_BOTTOM = int(SCREEN_H * BOTTOM_PCT)
MARGIN_LEFT = PANEL_WIDTH
MARGIN_RIGHT = PANEL_WIDTH

usable_w = SCREEN_W - (MARGIN_LEFT + MARGIN_RIGHT)
usable_h = SCREEN_H - (MARGIN_TOP + MARGIN_BOTTOM)

TILE_SIZE = min(usable_w // COLS, usable_h // ROWS)

GRID_W = COLS * TILE_SIZE
GRID_H = ROWS * TILE_SIZE

OFFSET_X = MARGIN_LEFT + (usable_w - GRID_W) // 2
OFFSET_Y = MARGIN_TOP + (usable_h - GRID_H) // 2
