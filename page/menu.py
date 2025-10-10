#####################
#FENETRE DEBUT DU JEU
#####################

import pygame


def run_menu(screen):
    # Définir les couleurs
    WHITE = (255, 255, 255)
    DARK_BLUE = (0, 80, 200)
    
    # Police pour le texte
    font = pygame.font.Font(None, 48)

    # Création bouton lancement du jeu
    launch_btn = pygame.Rect(
        screen.get_width() // 2 - 150,
        screen.get_height() // 2 - 40,
        300,
        80
    )

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            # Check les boutons cliqués
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si bouton lanchement cliqué
                if launch_btn.collidepoint(event.pos):
                    print("\nLancement du jeu.")
                    return 'game'

        # Dessiner l'écran
        screen.fill(WHITE)
        
        # Dessiner le bouton
        pygame.draw.rect(screen, DARK_BLUE, launch_btn, border_radius=12)
        text = font.render("Lancer le jeu", True, WHITE)
        text_rect = text.get_rect(center= launch_btn.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

    return None