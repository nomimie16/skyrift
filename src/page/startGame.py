########################
# FENETRE DEBUT DU JEU #
########################

import pygame
from src.const import *
from src.page.ui_components import Button


def run_start(screen):

    try:
        cursor_image = pygame.image.load("src/assets/img/cursor_orange.png")
        cursor_surf = pygame.transform.smoothscale(cursor_image, (32, 32))
        cursor = pygame.cursors.Cursor((0, 0), cursor_surf)
        pygame.mouse.set_cursor(cursor)
    except ValueError:
        print("Le curseur n'a pas pu être modifié")

    # Images
    fond = pygame.image.load(IMG_BG_START)
    fond = pygame.transform.scale(fond, (screen.get_width(), screen.get_height()))
    
    
    # Logo Skyrift
    logo = pygame.image.load(IMG_LOGO_TITRE).convert_alpha()
    logo = pygame.transform.scale(logo, (576, 305))
    logo_rect = logo.get_rect(center=(screen.get_width() // 2, 150))
    

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
        Button("Lancer le jeu", center_x, 320, "choosePlayer", TRANSLUCENT_BLUE, HOVER_BLUE, WHITE),
        Button("Options", center_x, 420, "settingsFromStart", TRANSLUCENT_BLUE, HOVER_BLUE, WHITE),
        Button("Règles", center_x, 520, "rulesFromStart", TRANSLUCENT_BLUE, HOVER_BLUE, WHITE),
        Button("Quitter", center_x, 620, "quit", TRANSLUCENT_BLUE, HOVER_BLUE, WHITE)
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
        screen.blit(logo, logo_rect)

        for button in buttons:
            button.draw(screen, mouse_pos, FONT_BUTTON)

        pygame.display.flip()

    return None
