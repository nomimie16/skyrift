########################
# FENETRE DE PARAMETRES #
########################

import pygame
from src.const import *
from src.page.ui_components import Button, Toggle
from src.component.sound import sound

music_on = True
sound_on = True

def run_settings(screen, background, from_game):
    global music_on, sound_on

    # Fond des settings
    bgSettings = pygame.image.load(IMG_BGSETTINGS).convert_alpha()
    bgSettings = pygame.transform.scale(bgSettings, (440, 200))
    bgSettings_rect = bgSettings.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Bouton retour au menu pause
    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2
    btn_retour = Button("Retour", center_x, center_y + 120, 'pause' if from_game else 'startGame', TRANSLUCENT_BLUE, HOVER_BLUE, WHITE)
    
    # Toggles Musique et Son
    toggles = [
        Toggle("Musique :", center_x + 125, center_y - 50),
        Toggle("Son du jeu :", center_x + 125, center_y + 40)
    ]
    
    # Etats des toggles
    toggles[0].is_on = music_on      
    toggles[1].is_on = sound_on 

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

        screen.blit(bgSettings, bgSettings_rect)

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
                            if toggle.label == "Musique :":
                                music_on = toggle.is_on
                                if music_on == False:
                                    sound.stop("music_menu")
                            elif toggle.label == "Son du jeu :":
                                if sound_on == False:
                                    sound.stop_all()
                    
                    # Clic dehors
                    if not bgSettings_rect.collidepoint(event.pos):
                        return 'pause' if from_game else 'startGame'

        pygame.display.flip()

    return None

def get_settings_states():
    return music_on, sound_on