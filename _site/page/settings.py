########################
#FENETRE DE PARAMETRES #
########################

import pygame

def run_settings(screen, background, from_game):
    # === COULEURS ===
    OVERLAY_COLOR = (0, 0, 0)
    OVERLAY_ALPHA = 150
    POPUP_COLOR = (240, 240, 240)
    BUTTON_COLOR = (0, 80, 200)
    BUTTON_TEXT_COLOR = (255, 255, 255)
    
    # === POLICE ===
    font = pygame.font.Font(None, 48)

    # === POP-UP CENTRALE ===
    popup_width, popup_height = 600, 400
    popup_rect = pygame.Rect(
        (screen.get_width()-popup_width)//2,
        (screen.get_height()-popup_height)//2,
        popup_width,
        popup_height
    )

    # === BOUTON RETOUR === 
    quit_settings = pygame.Rect(
        screen.get_width() // 2 - 125,
        screen.get_height() // 2 + 120,
        250,
        60
    )
    
    # === IMAGES TOGGLE MUSIQUE ===
    toggle_size = (80,70)
    img_music_toggle_off = pygame.image.load("assets/img/off_song_toggle.png").convert_alpha()
    img_music_toggle_off = pygame.transform.scale(img_music_toggle_off, toggle_size)
    img_music_toggle_off_rect = img_music_toggle_off.get_rect()
    img_music_toggle_off_rect.topleft = (
        screen.get_width() // 2-50,
        screen.get_height() // 2-110
    )
    img_music_toggle_on = pygame.image.load("assets/img/on_song_toggle.png").convert_alpha()
    img_music_toggle_on = pygame.transform.scale(img_music_toggle_on, toggle_size)
    img_music_toggle_on_rect = img_music_toggle_on.get_rect()
    img_music_toggle_on_rect.topleft = (
        screen.get_width() // 2-50,
        screen.get_height() // 2-110
    )
    # === IMAGES TOGGLE SON ===
    img_sound_toggle_off = pygame.image.load("assets/img/off_song_toggle.png").convert_alpha()
    img_sound_toggle_off = pygame.transform.scale(img_sound_toggle_off, toggle_size)
    img_sound_toggle_off_rect = img_sound_toggle_off.get_rect()
    img_sound_toggle_off_rect.topleft = (
        screen.get_width() // 2-50,
        screen.get_height() // 2 - 30
    )
    img_sound_toggle_on = pygame.image.load("assets/img/on_song_toggle.png").convert_alpha()
    img_sound_toggle_on = pygame.transform.scale(img_sound_toggle_on, toggle_size)
    img_sound_toggle_on_rect = img_sound_toggle_on.get_rect()
    img_sound_toggle_on_rect.topleft = (
        screen.get_width() // 2-50,
        screen.get_height() // 2 - 30
    )


    # === ETAT DU SON ===
    music_on = False
    sound_on = False

    # Tant que le jeu tourne
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        
        # === AFFICHAGE ===
        # Fond de la scène précedente (jeu ou menu)
        screen.blit(background, (0,0))
        
        # Overlay noir semi-transparent
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(OVERLAY_ALPHA)
        overlay.fill(OVERLAY_COLOR)
        screen.blit(overlay, (0,0))

        # Fenêtre pop-up
        pygame.draw.rect(screen, POPUP_COLOR, popup_rect, border_radius=20)

        # Bouton retour au menu pause
        pygame.draw.rect(screen, BUTTON_COLOR, quit_settings, border_radius=12)
        text = font.render("Retour", True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center= quit_settings.center)
        screen.blit(text, text_rect)
        
        # Titre du menu
        title = font.render("Paramètres", True, (0, 0, 0))
        title_rect = title.get_rect(center=(screen.get_width() // 2, popup_rect.top + 60))
        screen.blit(title, title_rect)
        
        # Label musique/son du jeu
        label_musique = font.render("Musique :", True, (0, 0, 0))
        label_rect = label_musique.get_rect(center=(screen.get_width() // 2 - 200, screen.get_height() // 2 - 70))
        screen.blit(label_musique, label_rect)
        label_son = font.render("Son du jeu :", True, (0, 0, 0))
        label_rect = label_son.get_rect(center=(screen.get_width() // 2 - 190, screen.get_height() // 2 + 20))
        screen.blit(label_son, label_rect)
        
        
        # Afficher le bon toggle selon l’état - SON et MUSIQUE
        if music_on:
            screen.blit(img_music_toggle_on, img_music_toggle_on_rect)
        else:
            screen.blit(img_music_toggle_off, img_music_toggle_off_rect)
        if sound_on:
            screen.blit(img_sound_toggle_on, img_sound_toggle_on_rect)
        else:
            screen.blit(img_sound_toggle_off, img_sound_toggle_off_rect)

        # Pour chaque évenement du jeu
        for event in pygame.event.get():
            # Check les boutons cliqués
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si bouton retour au jeu est cliqué
                if quit_settings.collidepoint(event.pos):
                    if from_game:
                        return 'pause'
                    else:
                        return 'startGame'
                if background.get_rect().collidepoint(event.pos) and not popup_rect.collidepoint(event.pos):
                    if from_game:
                        return 'pause'
                    else:
                        return 'startGame'
            
                # Toggle musique ON/OFF
                if img_music_toggle_off_rect.collidepoint(event.pos):
                    music_on = not music_on
                    print("Musique :", "ON" if music_on else "OFF")
                # Toggle son du jeu ON/OFF
                if img_sound_toggle_off_rect.collidepoint(event.pos):
                    sound_on = not sound_on
                    print("Son du jeu :", "ON" if sound_on else "OFF")
                    
        pygame.display.flip()

    return None