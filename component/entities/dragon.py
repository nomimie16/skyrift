import os
from typing import List

import pygame

import screen_const as sc
from component.entities.entity import Entity
from component.enum.type_entities import TypeEntitiesEnum
from component.grid import Cell, Grid
from component.position import Position
from const import DRAGONNET_COST, DRAGON_MOYEN_COST, DRAGON_GEANT_COST


class Dragon(Entity):

    def __init__(self, x_cell: int, y_cell: int, name: str, type_entity: List[TypeEntitiesEnum], max_hp: int,
                 attack_range: int, sprite_path: str,
                 speed: int,
                 attack_damage: int,
                 cost: int):
        super().__init__(x_cell, y_cell, name, type_entity, max_hp, attack_damage, attack_range, sprite_path)
        self._speed_base: int = speed  # speed de base du dragon
        self._actual_speed: int = speed  # speed actuel du dragon
        self._speed_modifier: int = 0  # nombre de speed en plus ou en moins à celui de base
        self._cost: int = cost
        self._index_img: int = 0
        self._moving: bool = False
        self._target_cell: Cell | None = None
        self._sprite_sheet = pygame.image.load(sprite_path)
        self._imageSprite = [self._sprite_sheet.subsurface(x * 64, 0, 64, 64) for x in range(4)]
        self._anim_counter = 0
        self._type: List[TypeEntitiesEnum] = [TypeEntitiesEnum.DRAGON]

    def reset_speed(self):
        """Réinitialise la vitesse à sa valeur de base."""
        self._actual_speed = self.base_speed
        self._speed_modifier = 0

    def move_dragon(self, target_x: int, target_y: int, grid: Grid):
        """
        Mouvement du dragon
        :param grid:
        :param target_x: (int) abscisse du nouvelle emplacement du drgaon
        :param target_y: (int) ordonnée du nouvelle emplacement du drgaon
        :return: None
        """
        self._target_cell = grid.cells[target_y][target_x]
        print(f"Déplacement du dragon {self.name} vers la cellule ({target_x}, {target_y})")
        self._moving = True

    def update(self, grid: Grid):
        """
        Met à jour la position du dragon lors de son déplacement
        :param grid: Grid
        :return: None
        """
        if not self._moving or not self._target_cell:
            return

        current_px = self.pixel_pos
        target_px = Position(
            self._target_cell.position.x * sc.TILE_SIZE + sc.OFFSET_X,
            self._target_cell.position.y * sc.TILE_SIZE + sc.OFFSET_Y
        )

        dx = target_px.x - current_px.x
        dy = target_px.y - current_px.y

        moved = False
        # mpuvement horizontal
        if dx != 0:
            moved = True
            if dx > 0:
                direction = 1
            else:
                direction = -1
            current_px.x += min(self._actual_speed, abs(dx)) * direction
            if direction > 0:
                self.update_direction("droite")
            else:
                self.update_direction("gauche")

        # mouvement vertical
        elif dy != 0:
            moved = True
            if dy > 0:
                direction = 1
            else:
                direction = -1
            current_px.y += min(self._actual_speed, abs(dy)) * direction

        # À l'arrivée
        if not moved:
            self._moving = False
            self._index_img = 0

            new_cell = grid.cells[self._target_cell.position.y][self._target_cell.position.x]
            #
            # old_cell = self.cell
            # old_cell.remove_occupant(self)
            self.cell = new_cell
            self._target_cell = None

            return

        self._anim_counter += 1
        if self._anim_counter >= 50:
            self._anim_counter = 0
            self._index_img = (self._index_img + 1) % len(self._imageSprite)

    def update_direction(self, direction: str):
        """
        Met à jour le sprite selon la direction du déplacement.
        :param direction: (str) direction du déplacement
        """
        base_path, filename = os.path.split(self.sprite_path)
        name, ext = os.path.splitext(filename)

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

        surface.blit(
            self._imageSprite[self._index_img],
            (
                int(self._pixel_pos.x + (sc.TILE_SIZE - self._imageSprite[self._index_img].get_width()) / 2),
                int(self._pixel_pos.y + (sc.TILE_SIZE - self._imageSprite[self._index_img].get_height()) / 2)
            )
        )

    # ------- Getters et Setters -------
    @property
    def speed_base(self) -> int:
        return self._speed_base

    @speed_base.setter
    def speed_base(self, value: int):
        self._speed_base = value

    @property
    def actual_speed(self) -> int:
        return self._actual_speed

    @actual_speed.setter
    def actual_speed(self, value: int):
        self._actual_speed = value

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
        super().__init__(x, y, name="Dragonnet",
                         type_entity=[TypeEntitiesEnum.DRAGONNET, TypeEntitiesEnum.DRAGON, TypeEntitiesEnum.OBSTACLE],
                         max_hp=50, attack_range=1,
                         sprite_path="assets/sprites/dragonnet/dragonnet_rouge_droite.png",
                         speed=6, attack_damage=10, cost=DRAGONNET_COST)


class DragonMoyen(Dragon):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, name="Dragon", type_entity=[TypeEntitiesEnum.DRAGON_MOYEN, TypeEntitiesEnum.DRAGON,
                                                           TypeEntitiesEnum.OBSTACLE],
                         max_hp=120, attack_range=2,
                         sprite_path="assets/sprites/dragon_moyen/dragon_moyen_rouge_droite.png",
                         speed=4, attack_damage=20, cost=DRAGON_MOYEN_COST)


class DragonGeant(Dragon):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, name="Dragon Géant",
                         type_entity=[TypeEntitiesEnum.DRAGON_GEANT, TypeEntitiesEnum.DRAGON,
                                      TypeEntitiesEnum.OBSTACLE], max_hp=250,
                         attack_range=3,
                         sprite_path="assets/sprites/dragon_geant/dragon_geant_bleu_droite.png",
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
