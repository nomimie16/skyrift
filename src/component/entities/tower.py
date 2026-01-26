import pygame

from src import screen_const as sc
from src.component.entities.entity import Entity
from src.component.grid import Grid
from src.enum.type_entities import TypeEntitiesEnum
from src.player import Player


class Tower(Entity):
    """
    Tour de défense
    """

    def __init__(self, x: int, y: int, sprite_path: str, player: Player = None):
        super().__init__(x, y, name="Tour de défense", type_entity=[TypeEntitiesEnum.TOWER, TypeEntitiesEnum.OBSTACLE],
                         max_hp=300,
                         attack_damage=25, attack_range=3,
                         sprite_path=sprite_path, kill_reward=90)
        self._width = 2
        self._height = 1
        self._player: Player = player
        self._active = False
        self._cost = 600
        self._attack_damage = 30
        self._attack_range = 5

    def future_position(self, x_start: int, y_base: int, target_height: int) -> list[tuple]:
        """
        Retourne les positions que la tour occupera une fois activée
        :param x_start: position x de la cellule la plus à gauche
        :param y_base: position y de la cellule la plus basse
        :param target_height: hauteur cible de la tour
        :return: liste de tuples (x, y)
        """
        future_occupied_positions = []
        for h in range(target_height):
            for w in range(self.width):
                pos_x = x_start + w
                pos_y = y_base - h
                future_occupied_positions.append((pos_x, pos_y))
        return future_occupied_positions

    def _clear_expansion_area(self, grid: Grid, player: Player, popup_manager):
        """
        Nettoie la zone d'expansion de la tour en infligeant des dégâts aux dragons
        :param popup_manager:
        :param player:
        :param grid: Grille sur laquelle est la tour
        :return: None
        """

        x_start = self.cell.position.x - (self.width - 1)
        y_base = self.cell.position.y
        target_height = 3

        future_occupied_positions = self.future_position(x_start, y_base, target_height)
        for y in range(y_base - 1, y_base - target_height, -1):
            for x in range(x_start, x_start + self.width):

                if not (0 <= x < grid.nb_columns and 0 <= y < grid.nb_rows):
                    continue

                cell_to_check = grid.cells[y][x]
                occupants = list(cell_to_check.occupants)

                for occ in occupants:
                    if occ == self:
                        continue

                    if TypeEntitiesEnum.PLAYER_EFFECT_ZONE in occ.type_entity:
                        amount = occ.amount
                        player.economy.earn_gold(amount)
                        cell_to_check.remove_occupant(occ)
                        occ.destroy()

                    elif TypeEntitiesEnum.DRAGON in occ.type_entity:

                        damage = 30
                        occ.take_damage(damage)
                        if popup_manager:
                            popup_manager.spawn_for_entity(occ, -damage)

                        grid.push_entity(occ, cell_to_check, ignored_positions=future_occupied_positions)

    def tower_activation(self, grid: Grid, player: Player, popup_manager=None) -> None:
        """
        Activation de la tour, elle peut attaquer
        :param popup_manager:
        :param player:
        :param grid: Grille sur laquelle est la tour
        :return: None
        """
        if self._active:
            return

        self._active = True
        self._height = 3
        self.set_sprite(f"src/assets/sprites/tour_{self.player.color}.png")
        print(self.sprite_path)

        self._clear_expansion_area(grid, player, popup_manager)
        grid.update_occupant_size(self)

    def tower_disable(self, grid: Grid) -> None:
        """
        Désactivation de la tour, elle reviens à son état de base
        :param grid: grille sur laquelle est là tour
        :return:
        """
        if self._active:
            self._active = False

        self._height = 1
        self._hp = self._max_hp
        self.set_sprite(f"src/assets/sprites/ile_vide.png")
        print(self.sprite_path)

        grid.update_occupant_size(self)

    def take_damage(self, amount) -> None:
        """
        Inflige des dégâts à la tour
        :param: amount: montant des dégâts
        :return: None
        """
        if self.active:
            self._hp = max(0, self._hp - amount)

    def draw(self, surface) -> None:
        """
        Dessine la tour à l'écran
        :param surface: Surface sur laquelle dessiner la tour
        :return: None
        """

        pixel_x = (self.cell.position.x - (self.width - 1)) * sc.TILE_SIZE + sc.OFFSET_X
        pixel_y = (self.cell.position.y - (self.height - 1)) * sc.TILE_SIZE + sc.OFFSET_Y

        scaled = pygame.transform.scale(
            self._sprite,
            (self.width * sc.TILE_SIZE, self.height * sc.TILE_SIZE)
        )

        surface.blit(scaled, (pixel_x, pixel_y))

        if self._active:
            self.draw_health_bar(surface, self.width, self.height - 1)

    @property
    def player(self) -> Player:
        return self._player

    @player.setter
    def player(self, value) -> None:
        self._player = value

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value

    @property
    def cost(self) -> int:
        return self._cost

    @property
    def attack_damage(self) -> int:
        return self._attack_damage

    @property
    def attack_range(self) -> int:
        return self._attack_range

    @property
    def image_sprite(self):
        return [self._sprite]
