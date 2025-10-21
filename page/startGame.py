######################
# FENETRE DEBUT DU JEU
######################

import pygame

def run_start(screen):
    # === COULEURS ===
    WHITE = (255, 255, 255)
    DARK_BLUE = (0, 80, 200)
    BLACK = (0, 0, 0)
    
    # === POLICES ===
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 42)

    # === BOUTON LANCEMENT ===
    launch_btn = pygame.Rect(
        screen.get_width() // 2 - 150,
        screen.get_height() // 2 + 100,
        300,
        80
    )
    
    # === CHOIX JOUEURS ===
    options = ["Jouer avec l'IA", "Jouer sans IA"]
    selected_index = 0

    running = True
    while running:
        for event in pygame.event.get():            
            # Gestion des flèches haut/bas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
            
            # Gestion clic souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                if launch_btn.collidepoint(event.pos):
                    print("\nLancement du jeu.")
                    #APPELER ICI LE JEU SELON IA OU NON!!!
                    # if selected_index == 0: 
                    #     return 'game_with_ia'
                    # else: 
                    #     return 'game_without_ia'
                    return 'game'

        # === AFFICHAGE ===
        screen.fill(WHITE)

        # Afficher les options de mode de jeu
        for i, option in enumerate(options):
            prefix = "> " if i == selected_index else "  "
            text_surface = small_font.render(prefix + option, True, BLACK)
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 80 + i * 50))
            screen.blit(text_surface, text_rect)

        # Bouton Lancer le jeu
        pygame.draw.rect(screen, DARK_BLUE, launch_btn, border_radius=12)
        text = font.render("Lancer le jeu", True, WHITE)
        text_rect = text.get_rect(center=launch_btn.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

    return None
