# ======================================
#  FICHIER DE CONSTANTES GLOBAL
# ======================================

import pygame

from pages import rules

# ----------------------------
# Couleurs
# ----------------------------
WHITE = (255, 255, 255)
TRANSLUCENT_BLUE = (0, 120, 200, 180)
HOVER_BLUE = (0, 140, 255, 220)
SHADOW = (0, 0, 0)
OVERLAY_COLOR = (0, 0, 0)
OVERLAY_ALPHA = 150
POPUP_COLOR = (240, 240, 240)
BUTTON_COLOR = (0, 80, 200)
BUTTON_TEXT_COLOR = (255, 255, 255)
TRANSLUCENT_RED = (200, 0, 0, 180)
HOVER_RED = (255, 0, 0, 220)

pygame.init()

# ----------------------------
# Images
# ----------------------------
startBackground = pygame.image.load('assets/img/bgStart.png')
rulesBackground = pygame.image.load('assets/img/bgRules.png')

# ----------------------------
# Polices
# ----------------------------
DEFAULT_FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 60)
try:
    FONT_TITLE = pygame.font.Font("assets/font/test1.ttf", 80)
    FONT_BUTTON = pygame.font.Font("assets/font/BoldPixels.ttf", 36)
except:
    FONT_TITLE = pygame.font.SysFont(None, 80)
    FONT_BUTTON = pygame.font.SysFont(None, 36)
