##########################
#FENETRE PRINCIPALE DU JEU
##########################

import pygame

def run_game(screen, ui):
    WHITE = (240, 240, 240)
    running = True
    
    img_test = pygame.image.load("assets/sprites/dragonnet.png").convert_alpha()
    img_test_rect = img_test.get_rect()
    img_test_rect.topleft = (100,100)

    while running:
        for event in pygame.event.get():
            #si on ferme la fenêtre
            if event.type == pygame.QUIT:
                return "quit"
            #
            action = ui.handle_event(event)
            if action == "quit":
                return "quit"
            if action == "settings":
                print("Ouvrir paramètres depuis le jeu")
                return "settings"

        #Dessiner le jeu 
        screen.fill(WHITE)
        ui.draw(screen)
        screen.blit(img_test,img_test_rect)
        pygame.display.flip()

    return None