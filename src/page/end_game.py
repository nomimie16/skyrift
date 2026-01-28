###################
# FENETRE DE FIN  #
###################

import pygame
from src.const import *
from src.page.ui_components import Button

def run_end_game(screen, background, winner_name):

    # Police
    title_font = pygame.font.Font(FONT_TITLE_PATH, 40)
    text_font = pygame.font.Font(FONT_TITLE_PATH, 20)
    button_font = pygame.font.Font(FONT_BUTTON_PATH, 48)

    # Image de fond
    bg_endGame = pygame.image.load(IMG_BG_END).convert_alpha()
    bg_endGame = pygame.transform.scale(bg_endGame, (screen.get_width(), screen.get_height()))

    # Image pop up
    bg_popup = pygame.image.load(IMG_BG_PAUSE).convert_alpha()
    bg_popup = pygame.transform.scale(bg_popup, (450, 600))
    bg_rect = bg_popup.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Image Victoire
    img_victory = pygame.image.load(IMG_VICTORY).convert_alpha()
    img_victory = pygame.transform.scale(img_victory, (300,150))
    img_victory_rect = img_victory.get_rect(
        center=(screen.get_width() // 2, bg_rect.top + 250)
    )

    # Boutons
    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2
    
    buttons = [
        Button("Rejouer", center_x, center_y + 50, "restart", TRANSLUCENT_BROWN, HOVER_BROWN, BROWN_FONT),
        Button("Menu Principal", center_x, center_y + 130, "startGame", TRANSLUCENT_BROWN, HOVER_BROWN, BROWN_FONT),
        Button("Quitter", center_x, center_y + 210, "quit", TRANSLUCENT_BROWN, HOVER_BROWN, BROWN_FONT)
    ]
    

    # === BOUCLE PRINCIPALE ===
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        return button.action

        # Fond de la scène précédente
        screen.blit(background, (0, 0))

        # Overlay noir semi-transparent
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(OVERLAY_ALPHA)
        overlay.fill(OVERLAY_COLOR)
        screen.blit(overlay, (0, 0))

        # Fond + popup + img vic
        screen.blit(bg_endGame, (0,0))
        screen.blit(bg_popup, bg_rect)
        screen.blit(img_victory, img_victory_rect)

        # ENTETE
        title_surf = title_font.render("FIN DE PARTIE", True, BROWN_FONT)
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, bg_rect.top + 100))
        screen.blit(title_surf, title_rect)

        winner_text = f"{winner_name} a gagne !"
        winner_surf = text_font.render(winner_text, True, BROWN_FONT)
        winner_rect = winner_surf.get_rect(center=(screen.get_width() // 2, bg_rect.top + 150))
        screen.blit(winner_surf, winner_rect)

        # Dessiner boutons
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.draw(screen, mouse_pos, button_font)

        pygame.display.flip()

    return 'quit'