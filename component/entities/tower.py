import pygame

import screen_const as sc
from component.entities.entity import Entity
from component.enum.type_entities import TypeEntitiesEnum
from component.grid import Grid
from player import Player


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

    def tower_activation(self, grid: Grid) -> None:
        """
        Activation de la tour, elle peut attaquer
        :param grid: Grille sur laquelle est la tour
        :return: None
        """
        if self._active:
            return

        old_width = self.width
        old_height = self.height

        self._active = True
        self._height = 3
        # TODO changer sprite
        self._sprite_path = f"assets/img/tour_{self.player.color}.png"

        grid.update_occupant_size(self, old_width, old_height)

    def tower_disable(self, grid: Grid) -> None:
        """
        Désactivation de la tour, elle reviens à son état de base
        :param grid: grille sur laquelle est là tour
        :return:
        """
        if self._active:
            self._active = False

        old_width = self.width
        old_height = self.height

        self._height = 1
        self._hp = 300
        # TODO changer sprites
        self._sprite_path = f"assets/img/tour_{self.player.color}.png"

        grid.update_occupant_size(self, old_width, old_height)

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
