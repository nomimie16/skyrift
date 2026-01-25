"""
Panneau de statistiques
"""
import pygame

from src.page.component.base_panel import BasePanel


class StatsPanel(BasePanel):
    """Panneau affichant les statistiques de la partie"""

    def __init__(self, width, x, y, height):
        super().__init__(width, x, y, height)

        # Cache icones
        self._icons_loaded = False
        self._hp_icon = None
        self._sword_icon = None

    def _load_icons(self):
        if self._icons_loaded:
            return

        try:
            hp_icon = pygame.image.load("src/assets/img/HP_icon.png").convert_alpha()
            self._hp_icon = pygame.transform.scale(hp_icon, (12, 12))
        except Exception:
            self._hp_icon = None

        try:
            sword_icon = pygame.image.load("src/assets/img/sword.png").convert_alpha()
            self._sword_icon = pygame.transform.scale(sword_icon, (12, 12))
        except Exception:
            self._sword_icon = None

        self._icons_loaded = True

    def _draw_wood_frame(self, surface):
        """Dessine le cadre"""
        super()._draw_wood_frame(surface)

        corner_size = 8
        line_y = self.y + 3
        for _ in range(3):
            pygame.draw.line(surface, self.WOOD_DARK, (self.x + corner_size, line_y),
                             (self.x + self.width - corner_size, line_y), 1)
            line_y += 1

        line_y = self.y + self.height - 6
        for _ in range(3):
            pygame.draw.line(surface, self.WOOD_DARK, (self.x + corner_size, line_y),
                             (self.x + self.width - corner_size, line_y), 1)
            line_y += 1

    def _count_dragons(self, player):
        return len(player.units)

    def draw(self, surface, turn, p1, p2, builder):
        """Dessine le panneau de statistiques"""
        self._load_icons()
        self._draw_wood_frame(surface)

        content_x = self.x + 10
        content_width = self.width - 20
        y = self.y + 14

        # Titre
        title = self.font_title.render("Statistiques", True, self.TEXT_DARK)
        title_rect = title.get_rect(centerx=self.x + self.width // 2, top=y)
        surface.blit(title, title_rect)
        y += 24

        self._draw_separator(surface, y)
        y += 10

        # infos partie
        section_title = self.font_normal.render("Partie", True, self.WOOD_DARK)
        surface.blit(section_title, (content_x, y))
        y += 18

        # n de tour
        turn_num = turn.get_turn_number() if hasattr(turn, 'get_turn_number') else turn.count if hasattr(turn, 'count') else "?"
        turn_text = self.font_small.render(f"Tour: {turn_num}", True, self.TEXT_DARK)
        surface.blit(turn_text, (content_x + 5, y))
        y += 16

        p1_color = (0, 100, 255)  # Bleu
        p1_dragons = self._count_dragons(p1)
        p1_text = self.font_small.render(f"{p1.name}: {p1_dragons} dragon(s)", True, p1_color)
        surface.blit(p1_text, (content_x + 5, y))
        y += 16

        p2_color = (200, 50, 50)  # Rouge
        p2_dragons = self._count_dragons(p2)
        p2_text = self.font_small.render(f"{p2.name}: {p2_dragons} dragon(s)", True, p2_color)
        surface.blit(p2_text, (content_x + 5, y))
        y += 20

        self._draw_separator(surface, y)
        y += 10

        # barre hp des bases
        section_title = self.font_normal.render("Bases", True, self.WOOD_DARK)
        surface.blit(section_title, (content_x, y))
        y += 18

        base1_hp = builder.base1.hp if builder.base1 else 0
        base1_max = builder.base1.max_hp if builder.base1 else 0
        self._draw_base_hp_bar(surface, content_x + 5, y, content_width - 10, base1_hp, base1_max, p1.name, p1_color)
        y += 28

        base2_hp = builder.base2.hp if builder.base2 else 0
        base2_max = builder.base2.max_hp if builder.base2 else 0
        self._draw_base_hp_bar(surface, content_x + 5, y, content_width - 10, base2_hp, base2_max, p2.name, p2_color)

    def _draw_base_hp_bar(self, surface, x, y, width, hp, max_hp, name, color):
        """Dessine une barre de vie avec le nom"""
        # Nom
        name_text = self.font_small.render(name[:12], True, color)
        surface.blit(name_text, (x, y))

        # Barre de vie
        bar_y = y + 18
        bar_height = 8
        bar_width = width - 80

        self._draw_hp_bar(surface, x, bar_y, bar_width, bar_height, hp, max_hp)

        # Texte HP
        hp_text = self.font_small.render(f"{hp}/{max_hp}", True, self.TEXT_DARK)
        surface.blit(hp_text, (x + bar_width + 4, bar_y - 1))
