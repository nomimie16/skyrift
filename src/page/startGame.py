########################
# FENETRE DEBUT DU JEU #
########################

import pygame
from src.const import *
from src.page.ui_components import Button


def run_start(screen):

    # Images
    fond = pygame.image.load(IMG_BG_START)
    fond = fond.convert()

    # Polices
    try:
        FONT_TITLE = pygame.font.Font(FONT_TITLE_PATH, 100)
        FONT_BUTTON = pygame.font.Font(FONT_BUTTON_PATH, 36)
    except:
        FONT_TITLE = pygame.font.SysFont(None, 100)
        FONT_BUTTON = pygame.font.SysFont(None, 36)

    # Récupérer la largeur de l'écran
    WIDTH_SCREEN = screen.get_width()
    center_x = WIDTH_SCREEN // 2

    # Boutons
    buttons = [
        Button("Lancer le jeu", center_x, 320, "game"),
        Button("Options", center_x, 420, "settingsFromStart"),
        Button("Règles", center_x, 520, "rulesFromStart"),
        Button("Quitter", center_x, 620, "quit")
    ]

    # ===== BOUCLE PRINCIPALE =====
    running = True
    while running:

        # Boucle d'événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("\nFermeture du jeu.")
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        print(f"Action : {button.action}")
                        return button.action

        screen.fill((0, 0, 0))

        screen.blit(fond, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Titre
        title = FONT_TITLE.render("SkyRift", True, WHITE)
        shadow = FONT_TITLE.render("SkyRift", True, SHADOW)
        screen.blit(shadow, (WIDTH_SCREEN // 2 - title.get_width() // 2 + 3, 103))
        screen.blit(title, (WIDTH_SCREEN // 2 - title.get_width() // 2, 100))

        for button in buttons:
            button.draw(screen, mouse_pos, FONT_BUTTON)

        pygame.display.flip()

    return None
