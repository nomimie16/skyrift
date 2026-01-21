###################
# FENETRE DE FIN  #
###################

import pygame
from src.const import *
from src.page.ui_components import Button

def run_end_game(screen, background, winner_name):

    # Police
    title_font = pygame.font.Font(None, 60)
    text_font = pygame.font.Font(None, 40)
    button_font = pygame.font.Font(None, 48)

    # Pop-up centrale
    popup_width, popup_height = 500, 400
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
        Button("Rejouer", center_x, center_y, "restart"),
        Button("Menu Principal", center_x, center_y + 80, "startGame"),
        Button("Quitter", center_x, center_y + 160, "quit")
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

        # Dessiner boutons
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.draw(screen, mouse_pos, button_font)

        pygame.display.flip()

    return 'quit'