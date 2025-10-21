##########################
#FENETRE PRINCIPALE DU JEU
##########################

import pygame

def run_game(screen, ui):
    WHITE = (240, 240, 240)
    running = True
    
    # pause_bg = pygame.image.load("assets/img/!!!!!!!!!!!!!!!!!.png").convert()
    # pause_bg = pygame.transform.scale(pause_bg, (screen.get_width(), screen.get_height()))
    
    img_test = pygame.image.load("assets/sprites/dragonnet.png").convert_alpha()
    img_test_rect = img_test.get_rect()
    img_test_rect.topleft = (100,100)

    while running:
        for event in pygame.event.get():
            action = ui.handle_event(event)
            if action == "pause":
                return "pause"

        #Dessiner le jeu 
        screen.fill(WHITE)
        ui.draw(screen)
        screen.blit(img_test,img_test_rect)
        # screen.blit(pause_bg, (0,0))
        pygame.display.flip()

    return None