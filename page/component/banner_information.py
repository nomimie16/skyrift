import pygame

from component.enum.event_enum import TypeEventEnum


class BannerInformation:
    """Classe représentant une bannière d'information pour afficher des événements à l'écran"""

    def __init__(self, event_description: TypeEventEnum | None, x=0, y=0, width=800, height=50):
        self.event_description = event_description
        self.display_time = 4000
        self.start_time = None
        self.active = False
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def show(self, event_description: TypeEventEnum) -> None:
        """
        Affiche la bannière avec la description de l'événement
        :param event_description:
        :return:
        """
        self.event_description = event_description
        self.start_time = pygame.time.get_ticks()
        self.active = True

    def draw(self, screen) -> None:
        """
        Dessine la bannière à l'écran
        :param screen:
        :return:
        """
        if not self.active:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.start_time <= self.display_time:
            banner_surface = pygame.Surface((self.width, self.height))
            banner_surface.set_alpha(200)
            banner_surface.fill((50, 50, 50))
            screen.blit(banner_surface, (self.x, self.y))

            font = pygame.font.Font(None, 36)
            text = font.render(f"{self.event_description.value}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text, text_rect)
        else:
            self.active = False
