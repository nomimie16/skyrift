import pygame
from .sidepanels import draw_sidepanels
from player import Player
from economy import Economy

def run_game(screen, ui, economy: Economy):
    WHITE = (240, 240, 240)
    running = True

    img_test = pygame.image.load("assets/sprites/dragonnet.png").convert_alpha()
    img_test_rect = img_test.get_rect()
    img_test_rect.topleft = (100,100)

    # Créer un joueur avec son économie
    player = Player()

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

        # Dessiner les sidebars et récupérer leurs positions et boutons
        left_rect, right_rect, current_left_x, current_right_x, buy_buttons = draw_sidepanels(
            screen, left_open, right_open, current_left_x, current_right_x, economy
        )

        for event in pygame.event.get():
            action = ui.handle_event(event)
            if action == "pause":
                return "pause"

            # Gérer les clics sur les boutons d'achat
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for button in buy_buttons:
                    if button["rect"].collidepoint(mouse_pos) and button["can_afford"]:
                        try:
                            economy.spend_gold(button["cost"])
                            print(f"{button["name"]} acheté! Or restant: {economy.get_gold()}")
                            player.add_unit(button["dragon"])
                            print(player.units)
                        except ValueError:
                            print("Pas assez d'or!")

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
