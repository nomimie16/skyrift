#####################
#FENETRE DEBUT DU JEU
#####################

import pygame
from src.const import *
from src.page.ui_components import Button


def run_menu(screen):
    
    # Police pour le texte
    font = pygame.font.Font(FONT_BUTTON_PATH, 48)

    # Création bouton lancement du jeu
    launch_btn = Button("Lancer le jeu", screen.get_width() // 2, screen.get_height() // 2, 'game', TRANSLUCENT_BLUE, HOVER_BLUE, WHITE)
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            # Check les boutons cliqués
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si bouton lanchement cliqué
                if launch_btn.collidepoint(event.pos):
                    return launch_btn.action

        # Dessiner l'écran
        screen.fill(WHITE)
        
        # Dessiner le bouton
        pos = pygame.mouse.get_pos()
        launch_btn.draw(screen, pos, font)

        pygame.display.flip()

    return None