########################
# FENETRE REGLE DU JEU #
########################

import pygame
from src.const import *

def run_rules(screen, from_game):

    # Image
    fond = pygame.image.load(IMG_BG_RULES).convert()
    fond = pygame.transform.scale(fond, (screen.get_width(), screen.get_height()))
    
    # Polices
    try:
        FONT_TITLE = pygame.font.Font(FONT_TITLE_PATH, 72)
        FONT_TEXT = pygame.font.Font(FONT_BUTTON_PATH, 36)
    except:
        FONT_TITLE = pygame.font.SysFont(None, 72)
        FONT_TEXT = pygame.font.SysFont(None, 36)
    
    # Texte "Retour au jeu"
    text = "Retour au jeu"
    text_pos = (screen.get_width() // 2, screen.get_height() - 80)
    
    # Image du fond du bouton
    bgButton = pygame.image.load(IMG_BGBUTTONRULES).convert_alpha()
    bgButton = pygame.transform.scale(bgButton, (400, 150))
    bgButton_rect = bgButton.get_rect(center=text_pos)

    # Image du livre
    livre = pygame.image.load(IMG_LIVRE).convert_alpha()
    livre = pygame.transform.scale(livre, (800, 450))
    livre_rect = livre.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
            
    # === BOUCLE PRINCIPALE ===
    running = True
    while running:
        
        mouse_pos = pygame.mouse.get_pos()

        # Dessiner le jeu
        screen.blit(fond, (0, 0))
        
        # Titre
        title = FONT_TITLE.render("Regles du jeu", True, WHITE)
        shadow = FONT_TITLE.render("Regles du jeu", True, SHADOW)
        screen.blit(shadow, (screen.get_width() // 2 - title.get_width() // 2 + 3, 103))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))

        # Txt back to game
        color = TRANSLUCENT_BLUE if bgButton_rect.collidepoint(mouse_pos) else (147, 96, 36, 0.8)
        text_surface = FONT_TEXT.render(text, True, color)
        text_rect = text_surface.get_rect(center=text_pos)

        # Dessiner le bouton retour
        screen.blit(bgButton, bgButton_rect)
        screen.blit(text_surface, text_rect)
        
        # Dessiner le livre
        screen.blit(livre, livre_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if bgButton_rect.collidepoint(event.pos):
                                    return 'game' if from_game else 'startGame'

        pygame.display.flip()

    return None