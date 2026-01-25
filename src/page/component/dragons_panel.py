"""
Panneau listant les dragons du joueur actif sous forme de grille
"""
import pygame

from src.component.entities.dragon import Dragon


class DragonsPanel:
    # Couleurs style bois
    WOOD_DARK = (101, 67, 33)
    WOOD_MEDIUM = (139, 90, 43)
    WOOD_LIGHT = (160, 120, 80)
    WOOD_INNER = (180, 140, 100)
    BEIGE_BG = (245, 235, 210)
    TEXT_DARK = (60, 40, 20)
    TEXT_ACCENT = (120, 80, 40)

    GRID_COLS = 3
    GRID_ROWS = 3

    def __init__(self, width, x, y, height):
        """
        Initialise le panneau de dragons.
        """
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.font_title = pygame.font.Font("src/assets/font/BoldPixels.ttf", 22)
        self.font_name = pygame.font.Font("src/assets/font/BoldPixels.ttf", 12)

        # Zones cliquables des dragons
        self.dragon_rects: list[tuple[pygame.Rect, Dragon]] = []

        self._update_cell_size()

    def set_position(self, x, y):
        """Met a jour la position du panneau"""
        self.x = x
        self.y = y

    def _update_cell_size(self):
        """Calcule la taille des cellules en fonction de l'espace disponible"""
        content_width = self.width - 20
        content_height = self.height - 75

        self.cell_width = content_width // self.GRID_COLS
        self.cell_height = content_height // self.GRID_ROWS

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

    def _draw_dragon_cell(self, surface, dragon: Dragon, x, y, is_selected: bool) -> pygame.Rect:
        """
        Dessine une cellule de dragon dans la grille.
        """
        cell_rect = pygame.Rect(x, y, self.cell_width - 4, self.cell_height - 4)

        # Fond de la cellule
        if is_selected:
            bg_color = (200, 180, 140)
        else:
            bg_color = (225, 215, 190)

        pygame.draw.rect(surface, bg_color, cell_rect)
        pygame.draw.rect(surface, self.WOOD_MEDIUM, cell_rect, 1)

        # Nom du dragon
        name_text = self.font_name.render(dragon.name, True, self.TEXT_DARK)
        name_rect = name_text.get_rect(centerx=cell_rect.centerx, top=cell_rect.top + 3)
        surface.blit(name_text, name_rect)

        # Barre de vie
        bar_width = self.cell_width - 16
        bar_height = 6
        bar_x = cell_rect.centerx - bar_width // 2
        bar_y = name_rect.bottom + 3
        pygame.draw.rect(surface, (100, 80, 60), (bar_x, bar_y, bar_width, bar_height))

        if dragon.max_hp > 0:
            hp_ratio = max(0, min(1, dragon.hp / dragon.max_hp))
            hp_width = int(bar_width * hp_ratio)

            if hp_ratio > 0.6:
                bar_color = (80, 160, 80)
            elif hp_ratio > 0.3:
                bar_color = (200, 160, 60)
            else:
                bar_color = (180, 60, 60)

            pygame.draw.rect(surface, bar_color, (bar_x, bar_y, hp_width, bar_height))

        pygame.draw.rect(surface, self.WOOD_DARK, (bar_x, bar_y, bar_width, bar_height), 1)

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
        """
        Dessine le panneau listant les dragons du joueur actif sous forme de grille.
        """
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
            no_dragons = self.font_name.render("Aucun dragon", True, self.TEXT_ACCENT)
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

            more_text = self.font_name.render(f"+ {remaining} autre(s)", True, self.TEXT_ACCENT)
            more_rect = more_text.get_rect(centerx=self.x + self.width // 2, top=separator_y + 6)
            surface.blit(more_text, more_rect)

    def handle_click(self, pos) -> Dragon | None:
        """
        Gere le clic sur le panneau.
        """
        for rect, dragon in self.dragon_rects:
            if rect.collidepoint(pos):
                return dragon
        return None
