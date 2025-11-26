import pygame
from sidepanels import draw_sidepanels

def run_game(screen, ui):
    WHITE = (240, 240, 240)
    running = True

    img_test = pygame.image.load("assets/sprites/dragonnet.png").convert_alpha()
    img_test_rect = img_test.get_rect()
    img_test_rect.topleft = (100,100)

    # État des panneaux
    left_open = False
    right_open = False

    # Position initiale des sidebars
    panel_width = 200
    current_left_x = -panel_width + 20
    current_right_x = screen.get_width() - 20

    while running:

        # Dessiner le jeu
        screen.fill(WHITE)
        ui.draw(screen)
        screen.blit(img_test, img_test_rect)

        # Dessiner les sidebars et récupérer leurs positions
        left_rect, right_rect, current_left_x, current_right_x = draw_sidepanels(
            screen, left_open, right_open, current_left_x, current_right_x
        )

        for event in pygame.event.get():
            action = ui.handle_event(event)
            if action == "pause":
                return "pause"

        # Gérer l'ouverture/fermeture des panneaux
        mouse = pygame.mouse.get_pos()
        if left_rect.collidepoint(mouse):
            left_open = True
        else:
            left_open = False

        if right_rect.collidepoint(mouse):
            right_open = True
        else:
            right_open = False

        pygame.display.flip()

    return None
