"""
Classe de base pour les panneaux avec style bois
"""
import pygame


class BasePanel:
    """
    Classe de base pour les panneaux style bois.
    Fournit le style visuel commun (cadre, separateurs, couleurs).
    """

    # Couleurs style bois
    WOOD_DARK = (101, 67, 33)
    WOOD_MEDIUM = (139, 90, 43)
    WOOD_LIGHT = (160, 120, 80)
    WOOD_INNER = (180, 140, 100)
    BEIGE_BG = (245, 235, 210)
    TEXT_DARK = (60, 40, 20)
    TEXT_ACCENT = (120, 80, 40)

    # Couleurs barre hp
    HP_COLOR_HIGH = (80, 160, 80)
    HP_COLOR_MEDIUM = (200, 160, 60)
    HP_COLOR_LOW = (180, 60, 60)
    HP_BAR_BG = (100, 80, 60)

    # Couleurs pour les statuts
    STATUS_POSITIVE = (80, 140, 80)
    STATUS_NEGATIVE = (150, 100, 100)

    FONT_PATH = "src/assets/font/BoldPixels.ttf"

    def __init__(self, width: int, x: int, y: int, height: int):
        """
        Initialise le panneau de base.
        """
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def set_position(self, x: int, y: int):
        """Met a jour la position du panneau"""
        self.x = x
        self.y = y

    def _draw_wood_frame(self, surface: pygame.Surface):
        """Dessine le cadre style bois"""
        border_size = 6

        # Cadre exterieur
        outer_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.WOOD_DARK, outer_rect)

        # Cadre intermediaire
        inner_rect1 = pygame.Rect(self.x + 2, self.y + 2, self.width - 4, self.height - 4)
        pygame.draw.rect(surface, self.WOOD_MEDIUM, inner_rect1)

        # Cadre interieur
        inner_rect2 = pygame.Rect(self.x + 4, self.y + 4, self.width - 8, self.height - 8)
        pygame.draw.rect(surface, self.WOOD_LIGHT, inner_rect2)

        # Fond beige
        bg_rect = pygame.Rect(self.x + border_size, self.y + border_size,
                              self.width - border_size * 2, self.height - border_size * 2)
        pygame.draw.rect(surface, self.BEIGE_BG, bg_rect)

        # Coins decoratifs
        self._draw_corners(surface)

    def _draw_corners(self, surface: pygame.Surface):
        """Dessine les coins decoratifs du cadre"""
        corner_size = 8

        pygame.draw.rect(surface, self.WOOD_DARK, (self.x, self.y, corner_size, corner_size))
        pygame.draw.rect(surface, self.WOOD_LIGHT, (self.x + 2, self.y + 2, corner_size - 4, corner_size - 4))

        pygame.draw.rect(surface, self.WOOD_DARK,
                         (self.x + self.width - corner_size, self.y, corner_size, corner_size))
        pygame.draw.rect(surface, self.WOOD_LIGHT,
                         (self.x + self.width - corner_size + 2, self.y + 2, corner_size - 4, corner_size - 4))

        pygame.draw.rect(surface, self.WOOD_DARK,
                         (self.x, self.y + self.height - corner_size, corner_size, corner_size))
        pygame.draw.rect(surface, self.WOOD_LIGHT,
                         (self.x + 2, self.y + self.height - corner_size + 2, corner_size - 4, corner_size - 4))

        pygame.draw.rect(surface, self.WOOD_DARK,
                         (self.x + self.width - corner_size, self.y + self.height - corner_size,
                          corner_size, corner_size))
        pygame.draw.rect(surface, self.WOOD_LIGHT,
                         (self.x + self.width - corner_size + 2, self.y + self.height - corner_size + 2,
                          corner_size - 4, corner_size - 4))

    def _draw_separator(self, surface: pygame.Surface, y: int, margin: int = 12):
        """Dessine un separateur"""
        pygame.draw.line(surface, self.WOOD_MEDIUM,
                         (self.x + margin, y),
                         (self.x + self.width - margin, y), 2)
        pygame.draw.line(surface, self.WOOD_LIGHT,
                         (self.x + margin, y + 1),
                         (self.x + self.width - margin, y + 1), 1)

    def _draw_hp_bar(self, surface: pygame.Surface, x: int, y: int, width: int, height: int,
                     current_hp: int, max_hp: int):
        """
        Dessine une barre de vie.
        """
        pygame.draw.rect(surface, self.HP_BAR_BG, (x, y, width, height))

        if max_hp > 0:
            hp_ratio = max(0, min(1, current_hp / max_hp))
            hp_width = int(width * hp_ratio)

            if hp_ratio > 0.6:
                bar_color = self.HP_COLOR_HIGH
            elif hp_ratio > 0.3:
                bar_color = self.HP_COLOR_MEDIUM
            else:
                bar_color = self.HP_COLOR_LOW

            pygame.draw.rect(surface, bar_color, (x, y, hp_width, height))
        else:
            bar_color = self.HP_COLOR_LOW

        pygame.draw.rect(surface, self.WOOD_DARK, (x, y, width, height), 1)

        return bar_color

    def _get_hp_color(self, current_hp: int, max_hp: int):
        """Retourne la couleur appropriee pour une barre de vie"""
        if max_hp <= 0:
            return self.HP_COLOR_LOW

        hp_ratio = current_hp / max_hp
        if hp_ratio > 0.6:
            return self.HP_COLOR_HIGH
        elif hp_ratio > 0.3:
            return self.HP_COLOR_MEDIUM
        else:
            return self.HP_COLOR_LOW

    def _create_font(self, size: int) -> pygame.font.Font:
        """Cree une police avec la taille specifiee"""
        return pygame.font.Font(self.FONT_PATH, size)
