########################
# FENETRE DEBUT DU JEU #
########################

from pygame import *
import pygame

def run_start(screen):
    # === RESSOURCES ===
    #Couleurs
    DARK_BLUE = (0, 80, 200)
    BLACK = (0, 0, 0)
    #Polices
    font = pygame.font.Font(None, 48)
    #Images
    fond = image.load('assets/img/bgPause.png')

    # === BOUTONS ===
    #Lancement
    launch_btn = pygame.Rect(
        screen.get_width() // 2 - 150,
        screen.get_height() // 2 - 100,
        300,
        80
    )
    #Quitter
    quit_btn = pygame.Rect(
        screen.get_width() // 2 - 150,
        screen.get_height() // 2 ,
        300,
        80
    )
    #Options
    options_btn = pygame.Rect(
        screen.get_width() // 2 - 150,
        screen.get_height() // 2 + 100,
        300,
        80
    )

    
    fond = fond.convert()

    running = True
    while running:
        # === AFFICHAGE ===
        screen.blit(fond, (0,0))
        
        # Bouton Lancer le jeu
        pygame.draw.rect(screen, DARK_BLUE, launch_btn, border_radius=12)
        text = font.render("Lancer le jeu", True, (255, 255, 255))
        text_rect = text.get_rect(center=launch_btn.center)
        screen.blit(text, text_rect)
        # Bouton Quitter
        pygame.draw.rect(screen, DARK_BLUE, quit_btn, border_radius=12)
        text = font.render("Quitter", True, (255, 255, 255))
        text_rect = text.get_rect(center=quit_btn.center)
        screen.blit(text, text_rect)
        # Bouton Options
        pygame.draw.rect(screen, DARK_BLUE, options_btn, border_radius=12)
        text = font.render("Options", True, (255, 255, 255))
        text_rect = text.get_rect(center=options_btn.center)
        screen.blit(text, text_rect)

        # === GESTION ÉVÉNEMENTS ===
        for event in pygame.event.get():            
            #pass
            
            # Gestion clic souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                if launch_btn.collidepoint(event.pos):
                    print("\nLancement du jeu.")
                    #appeler la pop up choix ia ou nn
                    return 'game'
                if quit_btn.collidepoint(event.pos):
                    print("\nFermeture du jeu.")
                    return 'quit'
                if options_btn.collidepoint(event.pos):
                    print("\nOuverture des options.")
                    return 'settingsFromStart'

        pygame.display.flip()

    return None