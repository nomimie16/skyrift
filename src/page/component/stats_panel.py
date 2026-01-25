"""
Panneau de statistiques
"""
import pygame


class StatsPanel:
    # Couleurs style bois
    WOOD_DARK = (101, 67, 33)       # Bord exterieur
    WOOD_MEDIUM = (139, 90, 43)    # Bord intermediaire
    WOOD_LIGHT = (160, 120, 80)    # Details du cadre
    WOOD_INNER = (180, 140, 100)   # Bord interieur
    BEIGE_BG = (245, 235, 210)     # Fond beige
    TEXT_DARK = (60, 40, 20)       # Texte principal
    TEXT_ACCENT = (120, 80, 40)    # Texte secondaire

    def __init__(self, width, x, y, height):
        """
        Initialise le panneau de statistiques.
        """
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.font_title = pygame.font.Font("src/assets/font/BoldPixels.ttf", 24)
        self.font_normal = pygame.font.Font("src/assets/font/BoldPixels.ttf", 18)
        self.font_small = pygame.font.Font("src/assets/font/BoldPixels.ttf", 15)

        # Caches icones
        self._icons_loaded = False
        self._hp_icon = None
        self._sword_icon = None

    def set_position(self, x, y):
        """Met a jour la position du panneau"""
        self.x = x
        self.y = y

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

        # ----- Details -----

        # Coins
        corner_size = 8
        corner_color = self.WOOD_DARK

        pygame.draw.rect(surface, corner_color, (self.x, self.y, corner_size, corner_size))
        pygame.draw.rect(surface, self.WOOD_LIGHT, (self.x + 2, self.y + 2, corner_size - 4, corner_size - 4))

        pygame.draw.rect(surface, corner_color, (self.x + self.width - corner_size, self.y, corner_size, corner_size))
        pygame.draw.rect(surface, self.WOOD_LIGHT,
                         (self.x + self.width - corner_size + 2, self.y + 2, corner_size - 4, corner_size - 4))

        pygame.draw.rect(surface, corner_color, (self.x, self.y + self.height - corner_size, corner_size, corner_size))
        pygame.draw.rect(surface, self.WOOD_LIGHT,
                         (self.x + 2, self.y + self.height - corner_size + 2, corner_size - 4, corner_size - 4))

        pygame.draw.rect(surface, corner_color,
                         (self.x + self.width - corner_size, self.y + self.height - corner_size, corner_size, corner_size))
        pygame.draw.rect(surface, self.WOOD_LIGHT,
                         (self.x + self.width - corner_size + 2, self.y + self.height - corner_size + 2,
                          corner_size - 4, corner_size - 4))

        # Lignes
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

    def _draw_separator(self, surface, y):
        margin = 12
        pygame.draw.line(surface, self.WOOD_MEDIUM,
                        (self.x + margin, y),
                        (self.x + self.width - margin, y), 2)
        pygame.draw.line(surface, self.WOOD_LIGHT,
                        (self.x + margin, y + 1),
                        (self.x + self.width - margin, y + 1), 1)

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
        self._draw_hp_bar(surface, content_x + 5, y, content_width - 10, base1_hp, base1_max, p1.name, p1_color)
        y += 28

        base2_hp = builder.base2.hp if builder.base2 else 0
        base2_max = builder.base2.max_hp if builder.base2 else 0
        self._draw_hp_bar(surface, content_x + 5, y, content_width - 10, base2_hp, base2_max, p2.name, p2_color)

    def _draw_hp_bar(self, surface, x, y, width, hp, max_hp, name, color):
        """Dessine une barre de vie avec le nom"""
        # Nom
        name_text = self.font_small.render(name[:12], True, color)
        surface.blit(name_text, (x, y))

        # Barre de vie
        bar_y = y + 18
        bar_height = 8
        bar_width = width - 80

        # Fond de la barre
        pygame.draw.rect(surface, (100, 80, 60), (x, bar_y, bar_width, bar_height))

        if max_hp > 0:
            hp_ratio = max(0, min(1, hp / max_hp))
            hp_width = int(bar_width * hp_ratio)

            # Couleur selon le pourcentage de vie
            if hp_ratio > 0.6:
                bar_color = (80, 160, 80)
            elif hp_ratio > 0.3:
                bar_color = (200, 160, 60)
            else:
                bar_color = (180, 60, 60)

            pygame.draw.rect(surface, bar_color, (x, bar_y, hp_width, bar_height))

        # Bordure
        pygame.draw.rect(surface, self.WOOD_DARK, (x, bar_y, bar_width, bar_height), 1)

        # Texte HP
        hp_text = self.font_small.render(f"{hp}/{max_hp}", True, self.TEXT_DARK)
        surface.blit(hp_text, (x + bar_width + 4, bar_y - 1))
