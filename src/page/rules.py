########################
# FENETRE REGLE DU JEU #
########################

import pygame
from src.const import *
from src.page.ui_components import Button

def run_rules(screen, from_game):

    # Image
    fond = pygame.image.load(IMG_BG_RULES)
    fond = fond.convert()

    # Polices
    try:
        FONT_TITLE = pygame.font.Font(FONT_TITLE_PATH, 72)
        FONT_BUTTON = pygame.font.Font(FONT_BUTTON_PATH, 36)
    except:
        FONT_TITLE = pygame.font.SysFont(None, 72)
        FONT_BUTTON = pygame.font.SysFont(None, 72)

    # Bouton
    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2
    action_retour = 'game' if from_game else 'startGame'
    btn_retour = Button("Retour", center_x, center_y + 300, action_retour, TRANSLUCENT_RED, HOVER_RED, WHITE)
            
    # === BOUCLE PRINCIPALE ===
    running = True
    while running:
        
        mouse_pos = pygame.mouse.get_pos()

        # Dessiner le jeu
        screen.blit(fond, (0, 0))
        btn_retour.draw(screen, mouse_pos, FONT_BUTTON)
        title = FONT_TITLE.render("Regles du jeu", True, WHITE)
        shadow = FONT_TITLE.render("Regles du jeu", True, SHADOW)
        screen.blit(shadow, (screen.get_width() // 2 - title.get_width() // 2 + 3, 103))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_retour.rect.collidepoint(event.pos):
                    return btn_retour.action

        pygame.display.flip()

    return None