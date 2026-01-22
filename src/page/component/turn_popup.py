import pygame
from src.const import FONT_BUTTON_PATH


class TurnPopup:
    """Classe représentant un popup pour indiquer le tour du joueur actuel"""

    def __init__(self, duration=2000, size=(400, 120), font_size=48):
        self.duration = duration
        self.size = size
        self.font_size = font_size

        self.active = False
        self.start_time = 0
        self.player_name = ""

        self.font = pygame.font.Font(FONT_BUTTON_PATH, self.font_size)

    def show(self, player_name) -> None:
        """
        Afficher le popup pour le joueur donné
        :param player_name: joueur actuel
        :return:
        """
        self.player_name = player_name
        self.start_time = pygame.time.get_ticks()
        self.active = True

    def draw(self, screen) -> None:
        """
        Dessiner le popup à l'écran
        :param screen:
        :return:
        """
        if not self.active:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.start_time <= self.duration:
            popup_surface = pygame.Surface(self.size)
            popup_surface.set_alpha(200)
            popup_surface.fill((0, 0, 0))
            popup_rect = popup_surface.get_rect(center=screen.get_rect().center)
            screen.blit(popup_surface, popup_rect)

            popup_text = self.font.render(f"Tour de {self.player_name}", True, (255, 255, 255))
            popup_text_rect = popup_text.get_rect(center=popup_rect.center)
            screen.blit(popup_text, popup_text_rect)
        else:
            self.active = False
