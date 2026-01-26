"""
Panneau listant les dragons du joueur actif sous forme de grille
"""
import pygame

from src.component.entities.dragon import Dragon
from src.page.component.base_panel import BasePanel


class DragonsPanel(BasePanel):
    """Panneau affichant la grille des dragons du joueur actif"""

    GRID_COLS = 3
    GRID_ROWS = 3

    CELL_BG = (225, 215, 190)
    CELL_BG_SELECTED = (200, 180, 140)

    def __init__(self, width, x, y, height):
        super().__init__(width, x, y, height)

        # Zones cliquables des dragons
        self.dragon_rects: list[tuple[pygame.Rect, Dragon]] = []

        self._update_cell_size()

    def _update_cell_size(self):
        """Calcule la taille des cellules en fonction de l'espace disponible"""
        content_width = self.width - 20
        content_height = self.height - 75

        self.cell_width = content_width // self.GRID_COLS
        self.cell_height = content_height // self.GRID_ROWS

    def _draw_dragon_cell(self, surface, dragon: Dragon, x, y, is_selected: bool) -> pygame.Rect:
        """Dessine une cellule de dragon dans la grille."""
        cell_rect = pygame.Rect(x, y, self.cell_width - 4, self.cell_height - 4)

        # Fond de la cellule
        bg_color = self.CELL_BG_SELECTED if is_selected else self.CELL_BG
        pygame.draw.rect(surface, bg_color, cell_rect)
        pygame.draw.rect(surface, self.WOOD_MEDIUM, cell_rect, 1)

        # Nom du dragon
        name_text = self.font_tiny.render(dragon.name, True, self.TEXT_DARK)
        name_rect = name_text.get_rect(centerx=cell_rect.centerx, top=cell_rect.top + 3)
        surface.blit(name_text, name_rect)

        # Barre de vie
        bar_width = self.cell_width - 16
        bar_height = 6
        bar_x = cell_rect.centerx - bar_width // 2
        bar_y = name_rect.bottom + 3

        self._draw_hp_bar(surface, bar_x, bar_y, bar_width, bar_height, dragon.hp, dragon.max_hp)

        # Icone du dragon
        if dragon.image_sprite:
            sprite = dragon.image_sprite[0]
            sprite_size = min(self.cell_width - 12, self.cell_height - 35)
            sprite_size = max(24, sprite_size)
            scaled_sprite = pygame.transform.smoothscale(sprite, (sprite_size, sprite_size))
            sprite_x = cell_rect.centerx - sprite_size // 2
            sprite_y = bar_y + bar_height + 4
            surface.blit(scaled_sprite, (sprite_x, sprite_y))

        return cell_rect

    def draw(self, surface, current_player, selected_dragon=None):
        """Dessine le panneau listant les dragons du joueur actif sous forme de grille."""
        self._draw_wood_frame(surface)

        self.dragon_rects = []

        content_x = self.x + 10
        y = self.y + 10

        # Titre
        title = self.font_title.render("Mes Dragons", True, self.TEXT_DARK)
        title_rect = title.get_rect(centerx=self.x + self.width // 2, top=y)
        surface.blit(title, title_rect)
        y += 22

        self._draw_separator(surface, y)
        y += 8

        # Liste des dragons du joueur actif
        dragons = current_player.units

        if not dragons:
            no_dragons = self.font_small.render("Aucun dragon", True, self.TEXT_ACCENT)
            no_rect = no_dragons.get_rect(centerx=self.x + self.width // 2, top=y + 30)
            surface.blit(no_dragons, no_rect)
            return

        grid_start_x = content_x
        grid_start_y = y

        max_dragons = self.GRID_COLS * self.GRID_ROWS

        for i, dragon in enumerate(dragons):
            if i >= max_dragons:
                break

            row = i // self.GRID_COLS
            col = i % self.GRID_COLS

            cell_x = grid_start_x + col * self.cell_width + 2
            cell_y = grid_start_y + row * self.cell_height + 2

            is_selected = (selected_dragon is not None and dragon == selected_dragon)
            cell_rect = self._draw_dragon_cell(surface, dragon, cell_x, cell_y, is_selected)
            self.dragon_rects.append((cell_rect, dragon))

        # Afficher + X autres si plus de 9 dragons
        remaining = len(dragons) - max_dragons
        if remaining > 0:
            separator_y = self.y + self.height - 28
            self._draw_separator(surface, separator_y)

            more_text = self.font_tiny.render(f"+ {remaining} autre(s)", True, self.TEXT_ACCENT)
            more_rect = more_text.get_rect(centerx=self.x + self.width // 2, top=separator_y + 6)
            surface.blit(more_text, more_rect)

    def handle_click(self, pos) -> Dragon | None:
        """Gere le clic sur le panneau."""
        for rect, dragon in self.dragon_rects:
            if rect.collidepoint(pos):
                return dragon
        return None
