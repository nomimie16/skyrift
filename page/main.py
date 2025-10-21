import pygame
from win32api import GetSystemMetrics # Récuperer la taille de l'écran
from startGame import run_start # Première fenêtre du jeu
from game import run_game # Fenêtre principale du jeu
from pause import run_pause # Page de pause
from settings import run_settings # Page de paramètres
from ui import UIOverlay # Import de l'interface commune du jeu

# Initialiser Pygame
pygame.init()

# Créer la fenêtre
taille_ecran = GetSystemMetrics(1)
screen = pygame.display.set_mode((taille_ecran, taille_ecran))

# Création de l'interface commune (icons)
ui = UIOverlay(screen)

# Lancer le menu
running = True
etat = 'menu'
background_game = None

while running:
    if etat == 'menu':
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

    elif etat == 'settings':
        background = screen.copy()
        etat = run_settings(screen, background)
        
    elif etat == 'quit':
        running = False

pygame.quit()
