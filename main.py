import pygame
from win32api import GetSystemMetrics # Récuperer la taille de l'écran
from pages.startGame import run_start # Première fenêtre du jeu
from pages.game import run_game # Fenêtre principale du jeu
from pages.pause import run_pause # Page de pause
from pages.settings import run_settings # Page de paramètres
from pages.rules import run_rules # Page des règles du jeu
from pages.sidepanels import draw_sidepanels # Import des panneaux latéraux du jeu
from pages.ui import UIOverlay # Import de l'interface commune du jeu

# Initialiser Pygame
pygame.init()

# Créer la fenêtre
taille_ecran = GetSystemMetrics(1)#hauteur de l'écran
screen = pygame.display.set_mode((taille_ecran, taille_ecran))
pygame.display.set_caption("SkyRift")

# Création de l'interface commune (icons)
ui = UIOverlay(screen)

# Lancer le menu
running = True
etat = 'startGame'
background_game = None

while running:
    if etat == 'startGame':
        etat = run_start(screen)

    elif etat == 'game':
        etat = run_game(screen, ui)
        background_game = screen.copy()

    elif etat == 'pause':
        if background_game is not None:
            background = background_game            
        else:
            background = screen.copy()
        etat = run_pause(screen, background)

    elif etat == 'settingsFromStart':
        background = screen.copy()
        etat = run_settings(screen, background, False)
        
    elif etat == 'settingsFromGame':
        background = screen.copy()
        etat = run_settings(screen, background, True)
        
    elif etat == 'rulesFromStart':
        etat = run_rules(screen, False)
    
    elif etat == 'rulesFromGame':
        etat = run_rules(screen, True)
            
    else:
        running = False

pygame.quit()