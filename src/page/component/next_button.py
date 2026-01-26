import pygame

from src.page.component.base_panel import BasePanel


class NextTurnButton(BasePanel):
    """Bouton 'Tour suivant' utilisant le style bois du BasePanel"""

    def __init__(self, x, y, width=160, height=50):
        super().__init__(width, x, y, height)
        self.rect = pygame.Rect(x, y, width, height)
        self.text = "Tour Suivant"

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, surface, enabled=True, hovered=False):
        """
        Dessine le bouton 'Tour Suivant' avec le style bois
        :param surface:
        :param enabled:
        :param hovered:
        :return:
        """
        self._draw_wood_frame(surface)

        if not enabled:
            overlay = pygame.Surface((self.width - 12, self.height - 12))
            overlay.fill((80, 80, 80))
            overlay.set_alpha(150)
            surface.blit(overlay, (self.x + 6, self.y + 6))

        elif hovered:
            overlay = pygame.Surface((self.width - 12, self.height - 12))
            overlay.fill((255, 255, 255))
            overlay.set_alpha(40)
            surface.blit(overlay, (self.x + 6, self.y + 6))
        font = self.font_title

        text_color = self.TEXT_DARK if enabled else (100, 100, 100)

        text_surf = font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)

        if enabled:
            shadow_surf = font.render(self.text, True, (180, 140, 100))
            surface.blit(shadow_surf, (text_rect.x + 1, text_rect.y + 1))

        surface.blit(text_surf, text_rect)
