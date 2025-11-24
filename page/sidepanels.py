#####################
# ONGLET SIDEPANELS #
#####################
import pygame

def draw_sidepanels(screen, left_open, right_open):
    panel_width = 200
    screen_height = screen.get_height()

    # Onglet gauche
    left_x = 0 if left_open else -panel_width + 20
    left_rect = pygame.Rect(left_x, 0, panel_width, screen_height)
    left_panel = pygame.Surface((panel_width, screen_height))
    left_panel.fill((50, 50, 50))
    screen.blit(left_panel, (left_x, 0))

    # Onglet droit
    right_x = screen.get_width() - panel_width if right_open else screen.get_width() - 20
    right_rect = pygame.Rect(right_x, 0, panel_width, screen_height)
    right_panel = pygame.Surface((panel_width, screen_height))
    right_panel.fill((50, 50, 50))
    screen.blit(right_panel, (right_x, 0))

    return left_rect, right_rect
