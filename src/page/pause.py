######################
# FENETRE MENU PAUSE #
######################

import pygame

from src.sound import Sound


def run_pause(screen, background):
    sound = Sound()
    # === COULEURS ===
    OVERLAY_COLOR = (0, 0, 0)
    OVERLAY_ALPHA = 150
    POPUP_COLOR = (240, 240, 240)
    BUTTON_COLOR = (0, 80, 200)
    BUTTON_TEXT_COLOR = (255, 255, 255)
    
    # === POLICE ===
    font = pygame.font.Font(None, 48)

    # === POP-UP CENTRALE ===
    popup_width, popup_height = 400, 500
    popup_rect = pygame.Rect(
        (screen.get_width() - popup_width) // 2,
        (screen.get_height() - popup_height) // 2,
        popup_width,
        popup_height
    )

    # === BOUTONS === 
    quit_pause = pygame.Rect(
        screen.get_width() // 2 - 125,
        screen.get_height() // 2 - 200,
        250,
        60
    )
    settings = pygame.Rect(
        screen.get_width() // 2 - 125,
        screen.get_height() // 2 - 100,
        250,
        60
    )
    rules_btn = pygame.Rect(
        screen.get_width() // 2 - 125,
        screen.get_height() // 2,
        250,
        60
    )
    quit_game = pygame.Rect(
        screen.get_width() // 2 - 125,
        screen.get_height() // 2 + 100,
        250,
        60
    )

    # === BOUCLE PRINCIPALE ===
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_pause.collidepoint(event.pos):
                    sound.play("temp.mp3")
                    return 'game'
                if quit_game.collidepoint(event.pos):
                    sound.play("temp.mp3")
                    return 'quit'
                if settings.collidepoint(event.pos):
                    sound.play("temp.mp3")
                    return 'settingsFromGame'
                if rules_btn.collidepoint(event.pos):
                    sound.play("temp.mp3")
                    return 'rulesFromGame'
                if background.get_rect().collidepoint(event.pos) and not popup_rect.collidepoint(event.pos):
                    sound.play("temp.mp3")
                    return 'game'

        # === AFFICHAGE ===
        # Fond de la scène précédente
        screen.blit(background, (0, 0))
        # Overlay noir semi-transparent
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(OVERLAY_ALPHA)
        overlay.fill(OVERLAY_COLOR)
        screen.blit(overlay, (0, 0))
        
        # Fenêtre pop-up
        pygame.draw.rect(screen, POPUP_COLOR, popup_rect, border_radius=20)
                
        # Bouton "Retour au jeu"
        pygame.draw.rect(screen, BUTTON_COLOR, quit_pause, border_radius=12)
        text = font.render("Retour au jeu", True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=quit_pause.center)
        screen.blit(text, text_rect)

        # Bouton "Paramètres"
        pygame.draw.rect(screen, BUTTON_COLOR, settings, border_radius=12)
        text = font.render("Paramètres", True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=settings.center)
        screen.blit(text, text_rect)
        
        # Bouton "Quitter le jeu"
        pygame.draw.rect(screen, BUTTON_COLOR, quit_game, border_radius=12)
        text = font.render("Quitter le jeu", True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=quit_game.center)
        screen.blit(text, text_rect)
        
        # Bouton "Règles du jeu"
        pygame.draw.rect(screen, BUTTON_COLOR, rules_btn, border_radius=12)
        text = font.render("Règles du jeu", True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=rules_btn.center)
        screen.blit(text, text_rect)
        
        pygame.display.flip()

    return None
