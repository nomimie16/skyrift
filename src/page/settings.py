########################
# FENETRE DE PARAMETRES #
########################

import pygame
from src.const import *
from src.page.ui_components import Button, Toggle

def run_settings(screen, background, from_game):

    # === POLICE ===
    font = pygame.font.Font(None, 48)

    # === POP-UP CENTRALE ===
    popup_width, popup_height = 600, 400
    popup_rect = pygame.Rect(
        (screen.get_width() - popup_width) // 2,
        (screen.get_height() - popup_height) // 2,
        popup_width,
        popup_height
    )

    # Bouton retour au menu pause
    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2
    btn_retour = Button("Retour", center_x, center_y + 120, 'pause' if from_game else 'startGame')
    
    # Toggles Musique et Son
    toggles = [
        Toggle("Musique :", center_x + 50, center_y - 70),
        Toggle("Son du jeu :", center_x + 50, center_y + 20)
    ]
    
    # Etats des toggles
    music_on = False
    sound_on = False

    # Tant que le jeu tourne
    running = True
    while running:
        mouse = pygame.mouse.get_pos()

        # === AFFICHAGE ===
        # Fond de la scène précedente (jeu ou menu)
        screen.blit(background, (0, 0))

        # Overlay noir semi-transparent
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(OVERLAY_ALPHA)
        overlay.fill(OVERLAY_COLOR)
        screen.blit(overlay, (0, 0))

        # Fenêtre pop-up
        pygame.draw.rect(screen, POPUP_COLOR, popup_rect, border_radius=20)

        # Titre du menu
        title = font.render("Paramètres", True, (0, 0, 0))
        title_rect = title.get_rect(center=(screen.get_width() // 2, popup_rect.top + 60))
        screen.blit(title, title_rect)

        # Afficher le bon toggle selon l’état - SON et MUSIQUE
        for toggle in toggles:
            toggle.draw(screen)

        # Pour chaque évenement du jeu
        for event in pygame.event.get():
            # Check les boutons cliqués
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle musique ON/OFF
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Bouton retour
                    if btn_retour.is_clicked(event.pos):
                        return btn_retour.action
                    
                    # Toggles
                    for toggle in toggles:
                        if toggle.is_clicked(event.pos):
                            toggle.toggle()
                    
                    # Clic dehors
                    if not popup_rect.collidepoint(event.pos):
                        return 'pause' if from_game else 'startGame'

        pygame.display.flip()

    return None
