import os

import pygame

from component.entities.entity import Entity
from component.position import Position
from const import DRAGONNET_COST, DRAGON_MOYEN_COST, DRAGON_GEANT_COST
from screen_const import TILE_SIZE


class Dragon(Entity):

    def __init__(self, x_cell: int, y_cell: int, name: str, max_hp: int, attack_range: int, sprite_path: str,
                 speed: int,
                 attack_damage: int,
                 cost: int):
        super().__init__(x_cell, y_cell, name, max_hp, attack_damage, attack_range, sprite_path)
        self.grid_pos = Position(x_cell, y_cell)  # position sur la grille
        self._pixel_pos = Position(x_cell * TILE_SIZE, y_cell * TILE_SIZE)  # position pour l'affichage
        self._speed_base: int = speed  # speed de base du dragon
        self._actual_speed: int = speed  # speed actuel du dragon
        self._speed_modifier: int = 0  # nombre de speed en plus ou en moins à celui de base
        self._cost: int = cost
        self._index_img: int = 0
        self._moving: bool = False
        self._target_cell: Position | None = None
        self._sprite_sheet = pygame.image.load(sprite_path)
        self._imageSprite = [self._sprite_sheet.subsurface(x * 64, 0, 64, 64) for x in range(4)]
        self._anim_counter = 0

    def reset_speed(self):
        """Réinitialise la vitesse à sa valeur de base."""
        self._actual_speed = self.base_speed
        self._speed_modifier = 0

    def move_dragon(self, x_cell: int, y_cell: int):
        """
        Mouvement du dragon
        :param x_cell: (int) abscisse du nouvelle emplacement du drgaon
        :param y_cell: (int) ordonnée du nouvelle emplacement du drgaon
        :return: None
        """
        self._target_cell = Position(x_cell, y_cell)
        self._moving = True

    def update(self):
        if not self._moving or not self._target_cell:
            return  # rien à faire si le dragon ne bouge pas

        target_x = self._target_cell.x * TILE_SIZE
        target_y = self._target_cell.y * TILE_SIZE

        dx = target_x - self._pixel_pos.x
        dy = target_y - self._pixel_pos.y

        if dx != 0:
            step_x = min(0.5, abs(dx)) * (1 if dx > 0 else -1)
            self._pixel_pos.x += step_x
            self.update_direction("droite" if dx > 0 else "gauche")
        elif dy != 0:
            step_y = min(0.5, abs(dy)) * (1 if dy > 0 else -1)
            self._pixel_pos.y += step_y

        if self._pixel_pos.x == target_x and self._pixel_pos.y == target_y:
            self._moving = False
            self.grid_pos.x = self._target_cell.x
            self.grid_pos.y = self._target_cell.y
            self._target_cell = None
            self._index_img = 0  # remettre sprite en position "repos"

        if self._moving:
            self._anim_counter += 1
            if self._anim_counter >= 50:
                self._anim_counter = 0
                self._index_img = (self._index_img + 1) % len(self._imageSprite)

    def update_direction(self, direction: str):
        """
        Met à jour le sprite selon la direction du déplacement.
        direction: 'gauche' ou 'droite'
        """
        base_path, filename = os.path.split(self.sprite_path)
        name, ext = os.path.splitext(filename)
        print("Base path:", base_path)
        print("Filename:", filename)
        print("Name:", name)
        print("Extension:", ext)

        print("Direction demandée:", direction)

        # On inverse le suffixe selon la direction
        if "gauche" not in name and direction == "gauche":
            new_name = name.replace("droite", "gauche")
        elif "droite" not in name and direction == "droite":
            new_name = name.replace("gauche", "droite")
        else:
            return

        new_path = f"{base_path}/{new_name}{ext}"
        new_path = new_path.replace("\\", "/")

        if os.path.exists(new_path):
            self._sprite_path = new_path
            self._sprite_sheet = pygame.image.load(new_path)
            self._imageSprite = [self._sprite_sheet.subsurface(x * 64, 0, 64, 64) for x in range(4)]

    def draw(self, surface):
        """
        Affichage du dragon
        @:param surface: Surface sur laquelle le dragon est placé
        """

        surface.blit(self._imageSprite[self._index_img], (int(self._pixel_pos.x), int(self._pixel_pos.y)))

    # ------- Getters et Setters -------
    @property
    def base_speed(self) -> int:
        return self._base_speed

    @base_speed.setter
    def base_speed(self, value: int):
        self._base_speed = value

    @property
    def attack_damage(self) -> int:
        return self._attack_damage

    @attack_damage.setter
    def attack_damage(self, value: int):
        self._attack_damage = value

    @property
    def attack_range(self) -> int:
        return self._attack_range

    @attack_range.setter
    def attack_range(self, value: int):
        self._attack_range = value

    @property
    def cost(self) -> int:
        return self._cost

    @cost.setter
    def cost(self, value: int):
        self._cost = value

    @property
    def movement_points(self) -> int:
        return self._movement_points

    @movement_points.setter
    def movement_points(self, value: int):
        self._movement_points = value

    @property
    def moving(self) -> bool:
        return self._moving

    @moving.setter
    def moving(self, value: bool):
        self._moving = value

    @property
    def target_place(self) -> Position | None:
        return self._target_place

    @target_place.setter
    def target_place(self, value: Position | None):
        self._target_place = value

    @property
    def index_img(self) -> int:
        return self._index_img

    @index_img.setter
    def index_img(self, value: int):
        self._index_img = value

    @property
    def image_sprite(self) -> list:
        return self._imageSprite

    @image_sprite.setter
    def image_sprite(self, value: list):
        self._imageSprite = value

    def __str__(self):
        return super().__str__()


class Dragonnet(Dragon):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, name="Dragonnet", max_hp=50, attack_range=1,
                         sprite_path="assets/sprites/dragonnet/dragonnet_rouge_droite.png",
                         speed=6, attack_damage=10, cost=DRAGONNET_COST)


class DragonMoyen(Dragon):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, name="Dragon", max_hp=120, attack_range=2,
                         sprite_path="assets/sprites/dragon_moyen/dragon_moyen_bleu_droite.png",
                         speed=4, attack_damage=20, cost=DRAGON_MOYEN_COST)


class DragonGeant(Dragon):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, name="Dragon Géant", max_hp=250, attack_range=3,
                         sprite_path="assets/sprites/dragon_geant.png",
                         speed=2, attack_damage=40, cost=DRAGON_GEANT_COST)


if __name__ == '__main__':
    # Création des dragons
    d1 = Dragonnet(0, 0)
    d2 = DragonMoyen(5, 10)
    d3 = DragonGeant(12, 3)

    print("=== TEST DRAGONS ===")
    print(f"Dragonnet -> Pos: {d1.position}, HP: {d1.hp}, Speed: {d1.speed}, Cost: {d1.cost}, Sprite: {d1.sprite_path}")
    print(
        f"Dragon Moyen -> Pos: {d2.position}, HP: {d2.hp}, Speed: {d2.speed}, Cost: {d2.cost}, Sprite: {d2.sprite_path}")
    print(
        f"Dragon Géant -> Pos: {d3.position}, HP: {d3.hp}, Speed: {d3.speed}, Cost: {d3.cost}, Sprite: {d3.sprite_path}")
