######################
#FENETRE DE PARAMETRES
######################

import pygame

def run_settings(screen, background):
    # Définir les couleurs
    OVERLAY_COLOR = (0, 0, 0)
    OVERLAY_ALPHA = 150
    POPUP_COLOR = (240, 240, 240)
    BUTTON_COLOR = (0, 80, 200)
    BUTTON_TEXT_COLOR = (255, 255, 255)
    
    # Police pour le texte
    font = pygame.font.Font(None, 48)
    
    # Pop-up centrale
    popup_width, popup_height = 600, 400
    popup_rect = pygame.Rect(
        (screen.get_width()-popup_width)//2,
        (screen.get_height()-popup_height)//2,
        popup_width,
        popup_height
    )

    # Création bouton retour au jeu
    quit_settings = pygame.Rect(
        screen.get_width() // 2 - 150,
        screen.get_height() // 2 - 40,
        200,
        80
    )

    running = True
    while running:
        
        for event in pygame.event.get():
            # Si fermeture de la fenêtre
            if event.type == pygame.QUIT:
                print('Fermeture du jeu.\n')
                return 'quit'
            # Check les boutons cliqués
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si bouton reour au jeu est cliqué
                if quit_settings.collidepoint(event.pos):
                    print("Retour au jeu.\n")
                    return 'game'

        # Fond assombri
        screen.blit(background, (0,0))  # affiche le menu ou le jeu
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(OVERLAY_ALPHA)
        overlay.fill(OVERLAY_COLOR)
        screen.blit(overlay, (0,0))  # assombrir le fond
        
        # Dessiner la pop-up
        pygame.draw.rect(screen, POPUP_COLOR, popup_rect, border_radius=20)
    

        # Dessiner le bouton
        pygame.draw.rect(screen, BUTTON_COLOR, quit_settings, border_radius=12)
        text = font.render("Retour au jeu", True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center= quit_settings.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

        


    return None