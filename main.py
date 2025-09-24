import pygame
from win32api import GetSystemMetrics # Récuperer la taille de l'écran
from menu import run_menu # Première fenêtre du jeu
from game import run_game # Fenêtre principale du jeu
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

while running:
    if etat == 'menu':
        etat = run_menu(screen, ui)
    elif etat == 'game':
       etat = run_game(screen, ui) 
    elif etat == 'settings':
        etat == 'menu'
        #page future
    elif etat == 'quit':
        running = False

pygame.quit()        
        
