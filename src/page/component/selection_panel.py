"""
Panneau affichant les statistiques du dragon selectionne
"""
import pygame

from src.component.entities.dragon import Dragon
from src.page.component.base_panel import BasePanel


class SelectionPanel(BasePanel):
    """Panneau affichant les stats du dragon selectionne"""

    def __init__(self, width, x, y, height):
        super().__init__(width, x, y, height)

        self.font_title = self._create_font(20)
        self.font_normal = self._create_font(16)
        self.font_small = self._create_font(14)

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

        self._draw_hp_bar(surface, bar_x, y + 2, bar_width, bar_height, dragon.hp, dragon.max_hp)

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
        moved_color = self.STATUS_NEGATIVE if dragon.has_moved else self.STATUS_POSITIVE
        moved_symbol = "X" if dragon.has_moved else "O"
        attacked_color = self.STATUS_NEGATIVE if dragon.has_attacked else self.STATUS_POSITIVE
        attacked_symbol = "X" if dragon.has_attacked else "O"

        move_text = self.font_small.render(f"Mvt: {moved_symbol}", True, moved_color)
        surface.blit(move_text, (stats_x, y))

        atk_text = self.font_small.render(f"Atk: {attacked_symbol}", True, attacked_color)
        surface.blit(atk_text, (stats_x + 80, y))
