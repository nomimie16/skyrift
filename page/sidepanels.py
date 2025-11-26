#####################
# ONGLET SIDEPANELS #
#####################
import pygame

def draw_sidepanels(screen, left_open, right_open, current_left_x, current_right_x):
    panel_width = 200
    screen_height = screen.get_height()
    animation_speed = 15

    # Calculer les positions cibles
    target_left_x = 0 if left_open else -panel_width + 20
    target_right_x = screen.get_width() - panel_width if right_open else screen.get_width() - 20

    # Animation gauche
    if current_left_x < target_left_x:
        current_left_x = min(current_left_x + animation_speed, target_left_x)
    elif current_left_x > target_left_x:
        current_left_x = max(current_left_x - animation_speed, target_left_x)

    # Animation droite
    if current_right_x < target_right_x:
        current_right_x = min(current_right_x + animation_speed, target_right_x)
    elif current_right_x > target_right_x:
        current_right_x = max(current_right_x - animation_speed, target_right_x)

    # Onglet gauche
    left_rect = pygame.Rect(current_left_x, 0, panel_width, screen_height)
    left_panel = pygame.Surface((panel_width, screen_height))
    left_panel.fill((50, 50, 50))
    screen.blit(left_panel, (current_left_x, 0))

    # Onglet droit
    right_rect = pygame.Rect(current_right_x, 0, panel_width, screen_height)
    right_panel = pygame.Surface((panel_width, screen_height))
    right_panel.fill((50, 50, 50))
    screen.blit(right_panel, (current_right_x, 0))

    return left_rect, right_rect, current_left_x, current_right_x
