import pygame

from src.sound import Sound


def run_end_game(screen, background, winner_name):
    sound = Sound()
    # === COULEURS ===
    OVERLAY_COLOR = (0, 0, 0)
    OVERLAY_ALPHA = 150
    POPUP_COLOR = (240, 240, 240)
    BUTTON_COLOR = (0, 80, 200)
    BUTTON_TEXT_COLOR = (255, 255, 255)
    TEXT_COLOR = (0, 0, 0)

    # === POLICE ===
    title_font = pygame.font.Font(None, 60)
    text_font = pygame.font.Font(None, 40)
    button_font = pygame.font.Font(None, 48)

    # === POP-UP CENTRALE ===
    popup_width, popup_height = 500, 400
    popup_rect = pygame.Rect(
        (screen.get_width() - popup_width) // 2,
        (screen.get_height() - popup_height) // 2,
        popup_width,
        popup_height
    )

    # === BOUTONS ===
    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2

    replay_btn = pygame.Rect(0, 0, 250, 60)
    replay_btn.center = (center_x, center_y + 0)

    menu_btn = pygame.Rect(0, 0, 250, 60)
    menu_btn.center = (center_x, center_y + 80)

    # 3. Bouton "Quitter"
    quit_btn = pygame.Rect(0, 0, 250, 60)
    quit_btn.center = (center_x, center_y + 160)

    # === BOUCLE PRINCIPALE ===
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_btn.collidepoint(event.pos):
                    sound.play("temp.mp3")
                    return 'restart'
                if menu_btn.collidepoint(event.pos):
                    sound.play("temp.mp3")
                    return 'startGame'
                if quit_btn.collidepoint(event.pos):
                    sound.play("temp.mp3")
                    return 'quit'

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

        # ENTETE
        title_surf = title_font.render("FIN DE PARTIE", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, popup_rect.top + 60))
        screen.blit(title_surf, title_rect)

        winner_text = f"{winner_name} a gagné !"
        winner_surf = text_font.render(winner_text, True, TEXT_COLOR)
        winner_rect = winner_surf.get_rect(center=(screen.get_width() // 2, popup_rect.top + 120))
        screen.blit(winner_surf, winner_rect)

        pygame.draw.rect(screen, BUTTON_COLOR, replay_btn, border_radius=12)
        text = button_font.render("Rejouer", True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=replay_btn.center)
        screen.blit(text, text_rect)

        # Bouton Menu Principal
        pygame.draw.rect(screen, BUTTON_COLOR, menu_btn, border_radius=12)
        text = button_font.render("Menu Principal", True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=menu_btn.center)
        screen.blit(text, text_rect)

        # Bouton "Quitter le jeu"
        pygame.draw.rect(screen, BUTTON_COLOR, quit_btn, border_radius=12)
        text = button_font.render("Quitter", True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=quit_btn.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

    return 'quit'
