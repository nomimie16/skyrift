"""
Panneau affichant les statistiques du dragon selectionne
"""
import pygame

from src.component.entities.dragon import Dragon


class SelectionPanel:
    # Couleurs style bois
    WOOD_DARK = (101, 67, 33)
    WOOD_MEDIUM = (139, 90, 43)
    WOOD_LIGHT = (160, 120, 80)
    WOOD_INNER = (180, 140, 100)
    BEIGE_BG = (245, 235, 210)
    TEXT_DARK = (60, 40, 20)
    TEXT_ACCENT = (120, 80, 40)

    def __init__(self, width, x, y, height):
        """
        Initialise le panneau de selection.
        """
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.font_title = pygame.font.Font("src/assets/font/BoldPixels.ttf", 20)
        self.font_normal = pygame.font.Font("src/assets/font/BoldPixels.ttf", 16)
        self.font_small = pygame.font.Font("src/assets/font/BoldPixels.ttf", 14)

    def set_position(self, x, y):
        """Met a jour la position du panneau"""
        self.x = x
        self.y = y

    def _draw_wood_frame(self, surface):
        """Dessine le cadre style bois"""
        border_size = 6

        outer_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.WOOD_DARK, outer_rect)

        inner_rect1 = pygame.Rect(self.x + 2, self.y + 2, self.width - 4, self.height - 4)
        pygame.draw.rect(surface, self.WOOD_MEDIUM, inner_rect1)

        inner_rect2 = pygame.Rect(self.x + 4, self.y + 4, self.width - 8, self.height - 8)
        pygame.draw.rect(surface, self.WOOD_LIGHT, inner_rect2)

        bg_rect = pygame.Rect(self.x + border_size, self.y + border_size,
                              self.width - border_size * 2, self.height - border_size * 2)
        pygame.draw.rect(surface, self.BEIGE_BG, bg_rect)

        # Coins decoratifs
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

    def _draw_separator(self, surface, y):
        margin = 12
        pygame.draw.line(surface, self.WOOD_MEDIUM,
                        (self.x + margin, y),
                        (self.x + self.width - margin, y), 2)
        pygame.draw.line(surface, self.WOOD_LIGHT,
                        (self.x + margin, y + 1),
                        (self.x + self.width - margin, y + 1), 1)

    def draw(self, surface, selected_dragon=None):
        """Dessine le panneau de selection"""
        self._draw_wood_frame(surface)

        content_x = self.x + 10
        content_width = self.width - 20
        y = self.y + 10

        # Titre
        title = self.font_title.render("Selection", True, self.TEXT_DARK)
        title_rect = title.get_rect(centerx=self.x + self.width // 2, top=y)
        surface.blit(title, title_rect)
        y += 22

        self._draw_separator(surface, y)
        y += 8

        if selected_dragon and isinstance(selected_dragon, Dragon):
            self._draw_dragon_stats(surface, content_x, y, content_width, selected_dragon)
        else:
            no_selection = self.font_small.render("Aucun dragon", True, self.TEXT_ACCENT)
            no_rect = no_selection.get_rect(centerx=self.x + self.width // 2, top=y + 20)
            surface.blit(no_selection, no_rect)

    def _draw_dragon_stats(self, surface, x, y, width, dragon):
        """Dessine les statistiques du dragon selectionne"""
        # Sprite du dragon
        if dragon.image_sprite:
            sprite = dragon.image_sprite[0]
            sprite_size = 36
            scaled_sprite = pygame.transform.smoothscale(sprite, (sprite_size, sprite_size))
            sprite_x = x + 5
            sprite_y = y
            surface.blit(scaled_sprite, (sprite_x, sprite_y))

            # Nom
            name_text = self.font_normal.render(dragon.name, True, self.TEXT_DARK)
            surface.blit(name_text, (sprite_x + sprite_size + 8, sprite_y + 3))

            # Proprietaire
            owner_color = (0, 100, 255) if dragon.player.color == "bleu" else (200, 50, 50)
            owner_text = self.font_small.render(f"({dragon.player.name})", True, owner_color)
            surface.blit(owner_text, (sprite_x + sprite_size + 8, sprite_y + 20))

            y += sprite_size + 6
        else:
            name_text = self.font_normal.render(dragon.name, True, self.TEXT_DARK)
            surface.blit(name_text, (x + 5, y))
            y += 18

        stats_x = x + 8

        # Barre HP
        hp_label = self.font_small.render("HP:", True, self.TEXT_ACCENT)
        surface.blit(hp_label, (stats_x, y))

        bar_x = stats_x + 25
        bar_width = width - 95
        bar_height = 8
        hp_ratio = max(0, min(1, dragon.hp / dragon.max_hp)) if dragon.max_hp > 0 else 0

        pygame.draw.rect(surface, (100, 80, 60), (bar_x, y + 2, bar_width, bar_height))

        if hp_ratio > 0.6:
            bar_color = (80, 160, 80)
        elif hp_ratio > 0.3:
            bar_color = (200, 160, 60)
        else:
            bar_color = (180, 60, 60)

        pygame.draw.rect(surface, bar_color, (bar_x, y + 2, int(bar_width * hp_ratio), bar_height))
        pygame.draw.rect(surface, self.WOOD_DARK, (bar_x, y + 2, bar_width, bar_height), 1)

        hp_value = self.font_small.render(f"{dragon.hp}/{dragon.max_hp}", True, self.TEXT_DARK)
        surface.blit(hp_value, (bar_x + bar_width + 4, y))
        y += 16

        # Stats
        stats_text = self.font_small.render(
            f"DMG: {dragon.attack_damage}  RNG: {dragon.attack_range}  SPD: {dragon.actual_speed}",
            True, self.TEXT_DARK
        )
        surface.blit(stats_text, (stats_x, y))
        y += 18

        # Status d'action
        moved_color = (150, 100, 100) if dragon.has_moved else (80, 140, 80)
        moved_symbol = "X" if dragon.has_moved else "O"
        attacked_color = (150, 100, 100) if dragon.has_attacked else (80, 140, 80)
        attacked_symbol = "X" if dragon.has_attacked else "O"

        move_text = self.font_small.render(f"Mvt: {moved_symbol}", True, moved_color)
        surface.blit(move_text, (stats_x, y))

        atk_text = self.font_small.render(f"Atk: {attacked_symbol}", True, attacked_color)
        surface.blit(atk_text, (stats_x + 80, y))
