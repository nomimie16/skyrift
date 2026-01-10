from typing import List

import pygame

from component.entities.dragon import Dragon
from component.entities.tower import Tower
from component.enum.type_entities import TypeEntitiesEnum
from component.grid import Grid, Cell
from component.position import Position
from screen_const import TILE_SIZE, OFFSET_X, OFFSET_Y


class TowerEvents:
    """
    Gère la sélection, les déplacements et les zones d'action des dragons
    Fonctionne avec un GridComponent ou toute grille avec cellules
    """

    def __init__(self, grid: Grid, origin: Position = (OFFSET_X, OFFSET_Y), tile_size=TILE_SIZE,
                 damage_heal_popup_manager=None):
        """
        :param grid: instance de Grid (la grille logique)
        :param origin: tuple (x, y) pour le coin supérieur gauche de la grille
        :param tile_size: taille d'une case en pixels
        """
        self.grid: Grid = grid
        self.origin: Position = origin
        self.tile_size = tile_size

        self.selected_tower: Tower | None = None

        self.attack_cells: list[Cell] = []

        self.attack_button_rect: pygame.Rect | None = None

        self.damage_heal_popup_manager = damage_heal_popup_manager

    def _pixel_to_cell(self, pos: Position) -> Position | None:
        """
        Convertit une position pixel (x,y) en Position (col,row) sur la grille
        :param pos: Position (x,y) en pixels
        :return: Position (col,row) ou None si hors grille
        """
        px, py = pos
        ox, oy = self.origin

        if px < ox or py < oy:
            return None

        col = (px - ox) // self.tile_size
        row = (py - oy) // self.tile_size

        if not (0 <= col < self.grid.nb_columns and 0 <= row < self.grid.nb_rows):
            return None

        return Position(col, row)

    def _reset_selection(self) -> None:
        """
        Réinitialise la sélection du dragon et les zones d'action
        :return:
        """
        self.selected_tower = None
        self.attack_cells = []
        self.attack_button_rect = None

    def compute_attack_dragons(self, tower: Tower) -> List[Dragon]:
        """
        Calcule toutes les cases attaquables pour la tour
        :param tower: instance de Tour
        :return: liste de Position des cases attaquables
        """
        dragons: List[Dragon] = []
        max_attack_range: int = tower.attack_range
        x0: int = tower.cell.position.x
        y0: int = tower.cell.position.y

        for y in range(self.grid.nb_rows):
            for x in range(self.grid.nb_columns):
                dist = abs(x - x0) + abs(y - y0)
                if 0 < dist <= max_attack_range:
                    cell = self.grid.cells[y][x]
                    for occupant in cell.occupants:
                        if TypeEntitiesEnum.DRAGON in occupant.type_entity and occupant.player != tower.player:
                            dragons.append(occupant)

        return dragons

    def handle_click(self, mouse_pos, occupant, player, turn):
        """
        Gère le clic de la souris pour la sélection des tours et l'attaque
        :param mouse_pos: Position (x,y) en pixels du clic
        :param occupant: Occupant de la cellule cliquée
        :param player: Joueur actuel
        :param turn: Tour actuel
        :return:
        """
        cell = Cell.get_cell_by_pixel(self.grid, mouse_pos)

        if self.attack_button_rect and self.attack_button_rect.collidepoint(mouse_pos):
            self.attack_all(turn)
            return

        if not cell:
            self._reset_selection()
            return

        if occupant and isinstance(occupant, Tower):
            if not occupant.active:
                print("Tour non activée")
                return
            if occupant.player != player:
                print("Ce n’est pas votre tour")
                return
            if turn and not turn.can_attack():
                print("Attaque déjà utilisée")
                return

            self.selected_tower = occupant
            self.attack_cells = self.compute_attack_dragons(occupant)
            return

        self._reset_selection()

    def attack_all(self, turn):
        """
        Attaque tous les dragons dans les zones d'attaque de la tour sélectionnée
        :param turn: Tour actuel
        :return:
        """
        if not self.selected_tower:
            return

        for dragon in self.attack_cells:
            dragon.take_damage(self.selected_tower.attack_damage)

            if self.damage_heal_popup_manager:
                self.damage_heal_popup_manager.spawn_for_entity(
                    dragon,
                    -self.selected_tower.attack_damage
                )

        if turn:
            turn.use_attack()

        self._reset_selection()

    def draw(self, surface) -> None:
        """
        Affiche les zones  d'attaque
        :param surface: surface pygame où dessiner
        :return: None
        """
        if not self.selected_tower:
            return

        # TODO Couleurs a revoir
        ox, oy = self.origin

        # Zones attaque
        for dragon in self.attack_cells:
            rect = pygame.Rect(
                ox + dragon.cell.position.x * self.tile_size,
                oy + dragon.cell.position.y * self.tile_size,
                self.tile_size,
                self.tile_size
            )
            pygame.draw.rect(surface, (255, 0, 0), rect, 3)

        if self.attack_cells:
            self.draw_attack_button(surface)

    def draw_attack_button(self, surface):
        """
        Dessine le bouton d'attaque au-dessus de la tour sélectionnée
        :param surface:
        :return:
        """
        if not self.selected_tower:
            self.attack_button_rect = None
            return

        ox, oy = self.origin
        col = self.selected_tower.cell.position.x
        row = self.selected_tower.cell.position.y

        button_width = 120
        button_height = 40

        tower_x = ox + col * self.tile_size
        tower_y = oy + row * self.tile_size

        x = tower_x + (self.tile_size - button_width) // 2
        y = tower_y - button_height - 8

        self.attack_button_rect = pygame.Rect(x, y, button_width, button_height)

        pygame.draw.rect(surface, (180, 50, 50), self.attack_button_rect)
        pygame.draw.rect(surface, (0, 0, 0), self.attack_button_rect, 2)

        font = pygame.font.Font(None, 24)
        text = font.render("ATTAQUER !!", True, (255, 255, 255))
        surface.blit(text, text.get_rect(center=self.attack_button_rect.center))
