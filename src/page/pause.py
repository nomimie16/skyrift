######################
# FENETRE MENU PAUSE #
######################

import pygame
from src.const import *
from src.page.ui_components import Button

def run_pause(screen, background):
    
    # Police
    font = pygame.font.Font(FONT_BUTTON_PATH, 48)

    # Image de fond
    bg_pause = pygame.image.load(IMG_BG_PAUSE).convert_alpha()
    bg_pause = pygame.transform.scale(bg_pause, (450, 550))
    bg_rect = bg_pause.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    # Boutons
    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2
    buttons = [
        Button("Retour au jeu", center_x, center_y - 150, "game", TRANSLUCENT_BROWN, HOVER_BROWN, BROWN_FONT),
        Button("Paramètres", center_x, center_y -50, "settingsFromGame", TRANSLUCENT_BROWN, HOVER_BROWN, BROWN_FONT),
        Button("Règles du jeu", center_x, center_y + 50, "rulesFromGame", TRANSLUCENT_BROWN, HOVER_BROWN, BROWN_FONT),
        Button("Quitter le jeu", center_x, center_y + 150, "quit", TRANSLUCENT_BROWN, HOVER_BROWN, BROWN_FONT)
    ]

    # === BOUCLE PRINCIPALE ===
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Vérifier les clics sur les boutons
                for button in buttons:
                    if button.is_clicked(event.pos):
                        return button.action
                
                # Clic en dehors de l'image de pause = retour au jeu
                if not bg_rect.collidepoint(event.pos):
                    return 'game'

        # Fond de la scène précédente
        screen.blit(background, (0, 0))
        # Overlay noir semi-transparent
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(OVERLAY_ALPHA)
        overlay.fill(OVERLAY_COLOR)
        screen.blit(overlay, (0, 0))
        
        # Fond du menu pause centré
        screen.blit(bg_pause, bg_rect)
        
        # Dessiner boutons
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.draw(screen, mouse_pos, font)
        
        pygame.display.flip()

    return None
