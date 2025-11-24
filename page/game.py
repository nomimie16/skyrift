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

    while running:
        
        # Dessiner le jeu
        screen.fill(WHITE)
        ui.draw(screen)
        screen.blit(img_test, img_test_rect)

        # Dessiner les side panels et récupérer leurs rectangles
        left_rect, right_rect = draw_sidepanels(screen, left_open, right_open)
        
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
