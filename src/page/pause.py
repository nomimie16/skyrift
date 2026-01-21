######################
# FENETRE MENU PAUSE #
######################

import pygame
from src.const import *
from src.page.ui_components import Button

def run_pause(screen, background):
    
    # Police
    font = pygame.font.Font(FONT_BUTTON_PATH, 48)

    # Pop-up
    popup_width, popup_height = 400, 500
    popup_rect = pygame.Rect(
        (screen.get_width() - popup_width) // 2,
        (screen.get_height() - popup_height) // 2,
        popup_width,
        popup_height
    )

    # Boutons
    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2
    buttons = [
        Button("Retour au jeu", center_x, center_y - 150, "game"),
        Button("Paramètres", center_x, center_y -50, "settingsFromGame"),
        Button("Règles du jeu", center_x, center_y + 50, "rulesFromGame"),
        Button("Quitter le jeu", center_x, center_y + 150, "quit")
    ]

    # === BOUCLE PRINCIPALE ===
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        return button.action
                if not popup_rect.collidepoint(event.pos):
                    return 'game'

        # Fond de la scène précédente
        screen.blit(background, (0, 0))
        # Overlay noir semi-transparent
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(OVERLAY_ALPHA)
        overlay.fill(OVERLAY_COLOR)
        screen.blit(overlay, (0, 0))
        
        # Fenêtre pop-up
        pygame.draw.rect(screen, POPUP_COLOR, popup_rect, border_radius=20)

        # Dessiner boutons
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.draw(screen, mouse_pos, font)
        
        pygame.display.flip()

    return None
