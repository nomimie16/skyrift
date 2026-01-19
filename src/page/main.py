import pygame

from src.page.end_game import run_end_game
from src.page.game import run_game  # Fenêtre principale du jeu
from src.page.launch import run_launch  # Introduction vidéo
from src.page.pause import run_pause  # Page de pause
from src.page.rules import run_rules  # Page des règles du jeu
from src.page.settings import run_settings  # Page de paramètres
from src.page.startGame import run_start  # Première fenêtre du jeu
from src.page.ui import UIOverlay  # Import de l'interface commune du jeu

# Initialiser Pygame
pygame.init()

# Créer la fenêtre
# screen = pygame.display.set_mode((SCREEN_H, SCREEN_H))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.display.set_caption("SkyRift")
# Création de l'interface commune (icons)
ui = UIOverlay(screen)

# Lancer le menu
running = True
etat = 'startGame'
background_game = None
winner_name = ""

while running:
    if etat == 'launch':
        etat = run_launch(screen)

    if etat == 'startGame':
        background_game = None
        etat = run_start(screen)

    elif etat == 'game':
        result = run_game(screen, ui)
        background_game = screen.copy()

        if isinstance(result, tuple) and result[0] == 'endGame':
            etat = 'endGame'
            winner_name = result[1]
        else:
            etat = result
    elif etat == 'endGame':
        if background_game is not None:
            background = background_game
        else:
            background = screen.copy()
        action = run_end_game(screen, background, winner_name)

        if action == 'restart':
            etat = 'game'
            background_game = None
        elif action == 'startGame':
            etat = 'startGame'
            background_game = None
        else:
            etat = 'quit'
            
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
