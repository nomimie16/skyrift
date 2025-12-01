from typing import List

import pygame

from component.entities.dragon import Dragon
from component.entities.entity import Entity
from component.entities.static_entity import StaticEntity
from component.enum.type_entities import TypeEntitiesEnum
from component.grid import Grid
from component.position import Position


# TODO logique d'attaque à implémenter
class DragonEvents:
    """
    Gère la sélection, les déplacements et les zones d'action des dragons
    Fonctionne avec un GridComponent ou toute grille avec cellules
    """

    def __init__(self, grid: Grid, origin: Position, tile_size):
        """
        :param grid: instance de Grid (la grille logique)
        :param origin: tuple (x, y) pour le coin supérieur gauche de la grille
        :param tile_size: taille d'une case en pixels
        """
        self.grid: Grid = grid
        self.origin: Position = origin
        self.tile_size = tile_size

        self.selected_dragon: Dragon | None = None
        self.move_cells: List = []
        self.attack_cells: List = []

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

    def display_move_cells(self, dragon: Dragon) -> List[Position]:
        """
        Calcule toutes les cases accessibles pour le dragon
        :param dragon: instance de Dragon
        :return: liste de Position des cases accessibles
        """
        max_move = dragon.actual_speed
        x0, y0 = dragon.grid_pos.x, dragon.grid_pos.y

        possible = []
        for y in range(self.grid.nb_rows):
            for x in range(self.grid.nb_columns):
                dist = abs(x - x0) + abs(y - y0)
                if 0 < dist <= max_move:
                    possible.append(Position(x, y))

        for pos in possible[:]:
            cell = self.grid.cells[pos.y][pos.x]
            if len(cell.occupants) > 0:
                if any(TypeEntitiesEnum.OBSTACLE in o.type_entity for o in cell.occupants):
                    possible.remove(pos)

        return possible

    def handle_click(self, mouse_pos: Position, occupant: Entity | StaticEntity | None = None):
        """
        Gère le clic sur la grille :
        - sélection d'un dragon
        - déplacement si dragon sélectionné
        @param mouse_pos: Position (x,y) du clic souris en pixels
        @param occupant: occupant de la case cliquée (s'il y en a un)
        @return: None
        """
        cell_pos: Position = self._pixel_to_cell(mouse_pos)
        if not cell_pos:
            return

        cell = self.grid.cells[cell_pos.y][cell_pos.x]

        # Clique sur un dragon
        if occupant and TypeEntitiesEnum.DRAGON in occupant.type_entity:
            if isinstance(occupant, Dragon):
                self.selected_dragon = occupant
            self.move_cells = self.display_move_cells(self.selected_dragon)
            self.attack_cells = []  # TODO à implémenter
            print(f"Dragon sélectionné -> {self.selected_dragon.name}")
            return

        # Clique sur case vide avec dragon sélectionné
        if self.selected_dragon:
            if any(p.x == cell_pos.x and p.y == cell_pos.y for p in self.move_cells):
                self.grid.remove_occupant(self.selected_dragon.grid_pos, self.selected_dragon)
                self.grid.add_occupant(self.selected_dragon, cell_pos)
                self.selected_dragon.move_dragon(cell_pos.x, cell_pos.y)
                print(self.grid)

            self.selected_dragon = None
            self.move_cells = []
            self.attack_cells = []

    def draw(self, surface):
        """
        Affiche les zones de déplacement et d'attaque
        :param surface: surface pygame où dessiner
        :return: None
        """
        # TODO Couleurs a revoir
        ox, oy = self.origin

        # Zones déplacement
        for pos in self.move_cells:
            rect = pygame.Rect(
                ox + pos.x * self.tile_size,
                oy + pos.y * self.tile_size,
                self.tile_size,
                self.tile_size
            )
            pygame.draw.rect(surface, (0, 100, 255), rect, 3)
