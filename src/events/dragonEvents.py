from typing import List

import pygame

from src.component.entities.dragon import Dragon
from src.component.entities.entity import Entity
from src.component.entities.static_entity import StaticEntity
from src.component.grid import Grid, Cell
from src.component.position import Position
from src.enum.type_entities import TypeEntitiesEnum
from src.player import Player
from src.component.sound import sound


class DragonEvents:
    """
    Gère la sélection, les déplacements et les zones d'action des dragons
    Fonctionne avec un GridComponent ou toute grille avec cellules
    """

    def __init__(self, grid: Grid, origin: Position, tile_size, damage_heal_popup_manager=None):
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
        self.selected_dragon = None
        self.move_cells = []
        self.attack_cells = []

    def select_dragon(self, dragon: Dragon, player: Player) -> None:
        """
        Sélectionne un dragon et calcule ses zones d'action
        """
        if dragon.player != player:
            print("Ce dragon n'appartient pas à votre joueur !")
            return

        self.selected_dragon = dragon

        if not self.selected_dragon.has_moved:
            self.move_cells = self.compute_move_cells(self.selected_dragon)
        else:
            self.move_cells = []

        if not self.selected_dragon.has_attacked:
            self.attack_cells = self.compute_attack_cells(self.selected_dragon)
        else:
            self.attack_cells = []

    def compute_move_cells(self, dragon: Dragon) -> List[Cell]:
        """
        Calcule toutes les cases accessibles pour le dragon
        :param dragon: instance de Dragon
        :return: liste de Position des cases accessibles
        """
        max_move = dragon.actual_speed
        start_x, start_y = dragon.cell.position.x, dragon.cell.position.y

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Droite, Gauche, Bas, Haut
        visited = set()
        possible_cells = []
        queue = [(start_x, start_y, 0)]  # liste = file FIFO
        visited.add((start_x, start_y))

        while queue:
            x, y, dist = queue.pop(0)

            if dist > 0:
                possible_cells.append(self.grid.cells[y][x])

            if dist == max_move:
                continue

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if not (0 <= nx < self.grid.nb_columns and 0 <= ny < self.grid.nb_rows):
                    continue

                if (nx, ny) in visited:
                    continue

                next_cell = self.grid.cells[ny][nx]

                blocked = False
                for occ in next_cell.occupants:
                    if TypeEntitiesEnum.OBSTACLE in occ.type_entity:
                        blocked = True
                        break

                if blocked:
                    continue

                visited.add((nx, ny))
                queue.append((nx, ny, dist + 1))

        return possible_cells

    def compute_attack_cells(self, dragon: Dragon) -> List[Cell]:
        """
        Calcule toutes les cases attaquables pour le dragon
        :param dragon: instance de Dragon
        :return: liste de Position des cases attaquables
        """
        max_attack_range: int = dragon.attack_range
        x0: int = dragon.cell.position.x
        y0: int = dragon.cell.position.y

        possible_cells: List[Cell] = []
        for y in range(self.grid.nb_rows):
            for x in range(self.grid.nb_columns):
                dist = abs(x - x0) + abs(y - y0)
                if 0 < dist <= max_attack_range:
                    cell = self.grid.cells[y][x]
                    for occupant in cell.occupants:
                        if TypeEntitiesEnum.DRAGON in occupant.type_entity and occupant.player != dragon.player:
                            possible_cells.append(cell)
                        if (TypeEntitiesEnum.BASE in occupant.type_entity and occupant.player != dragon.player):
                            possible_cells.append(cell)
                        if (
                                TypeEntitiesEnum.TOWER in occupant.type_entity and occupant._active and occupant.player != dragon.player):
                            possible_cells.append(cell)

        return possible_cells

    def handle_click(self, mouse_pos: Position, occupant: Entity | StaticEntity | None = None, player: Player = None,
                     turn=None):
        """
        Gère le clic sur la grille :
        - sélection d'un dragon
        - déplacement si dragon sélectionné
        :param mouse_pos: Position (x,y) du clic souris en pixels
        :param occupant: occupant de la case cliquée (s'il y en a un)
        :param player: joueur effectuant l'action
        :param turn: instance de Turn pour vérifier les restrictions d'actions
        :return: None
        """
        cell = Cell.get_cell_by_pixel(self.grid, mouse_pos)
        if not cell:
            return

        # Clique sur case avec dragon sélectionné
        if self.selected_dragon:
            attacked: bool = False

            # Déplacement
            if cell in self.move_cells:
                if self.selected_dragon.has_moved:
                    print("Ce dragon s'est déjà déplacé durant le tour !")
                    self._reset_selection()
                    return

                current_cell = self.grid.cells[self.selected_dragon.cell.position.y][
                    self.selected_dragon.cell.position.x]

                current_cell.remove_occupant(self.selected_dragon)
                self.grid.add_occupant(self.selected_dragon, cell)
                self.selected_dragon.move_dragon(cell.position.x, cell.position.y, self.grid)

                self.selected_dragon.has_moved = True
                print(f"Dragon déplacé - Déplacement utilisé pour ce dragon")

            # Attaque
            if cell in self.attack_cells:
                if self.selected_dragon.has_attacked:
                    print("Ce dragon a déjà attaqué durant le tour !")
                    self._reset_selection()
                    return

                for occupant in cell.occupants:
                    if (
                            TypeEntitiesEnum.DRAGON in occupant.type_entity
                            or TypeEntitiesEnum.BASE in occupant.type_entity
                            or TypeEntitiesEnum.TOWER in occupant.type_entity
                    ) and occupant.player != player:

                        if TypeEntitiesEnum.TOWER in occupant.type_entity:
                            if hasattr(occupant, '_active') and not occupant._active:
                                continue

                        damage = self.selected_dragon.attack_damage
                        occupant.last_attacker = player
                        occupant.take_damage(damage)
                        self.selected_dragon.attack_fireball(occupant)
                        sound.play("fireball_attack.wav")  # attaque de dragon

                        if self.damage_heal_popup_manager:
                            self.damage_heal_popup_manager.spawn_for_entity(occupant, -damage)

                        attacked = True

                if attacked:
                    self.selected_dragon.has_attacked = True
                    print(f"Attaque effectuée - Attaque utilisée pour ce dragon")

            self.selected_dragon = None

            if attacked:
                self.move_cells = []
                self.attack_cells = []
                return
        self.move_cells = []
        self.attack_cells = []

        # Clique sur un dragon
        if occupant and TypeEntitiesEnum.DRAGON in occupant.type_entity:
            if isinstance(occupant, Dragon):
                # Vérifier que le dragon appartient au joueur actuel
                if player is not None and occupant.player != player:
                    print("Ce dragon n'appartient pas à votre joueur !")
                    return
                self.selected_dragon = occupant

                # One ne montre les cellules que si le joueur peut encore bouger
                if not self.selected_dragon.has_moved:
                    self.move_cells = self.compute_move_cells(self.selected_dragon)
                else:
                    self.move_cells = []
                    if not self.selected_dragon.has_moved:
                        print("Vous avez déjà déplacé un dragon ce tour !")

                # De même que pour le mouvement, on ne montre les cellules d'attaque que si le joueur peut encore attaquer
                if not self.selected_dragon.has_attacked:
                    self.attack_cells = self.compute_attack_cells(self.selected_dragon)
                else:
                    self.attack_cells = []
                    if self.selected_dragon.has_attacked:
                        print("Vous avez déjà attaqué ce tour !")
            return

    def draw(self, surface) -> None:
        """
        Affiche les zones de déplacement et d'attaque
        :param surface: surface pygame où dessiner
        :return: None
        """
        # TODO Couleurs a revoir
        ox, oy = self.origin

        # Zones déplacement
        for cell in self.move_cells:
            rect = pygame.Rect(
                ox + cell.position.x * self.tile_size,
                oy + cell.position.y * self.tile_size,
                self.tile_size,
                self.tile_size
            )
            pygame.draw.rect(surface, (0, 100, 255), rect, 3)

            # Zones effet
            for occ in cell.occupants:
                if TypeEntitiesEnum.BAD_EFFECT_ZONE in occ.type_entity:
                    pygame.draw.rect(surface, (255, 128, 0), rect, 3)
                if TypeEntitiesEnum.GOOD_EFFECT_ZONE in occ.type_entity:
                    pygame.draw.rect(surface, (0, 255, 0), rect, 3)

        # Zones attaque
        for cell in self.attack_cells:
            rect = pygame.Rect(
                ox + cell.position.x * self.tile_size,
                oy + cell.position.y * self.tile_size,
                self.tile_size,
                self.tile_size
            )
            pygame.draw.rect(surface, (255, 0, 0), rect, 3)
