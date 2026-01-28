import os
from typing import List

import pygame

from src import screen_const as sc
from src.component.entities.entity import Entity
from src.component.entities.fireball import Fireball
from src.component.grid import Cell, Grid
from src.component.path_finding import find_path
from src.component.position import Position
from src.component.sound import sound
from src.const import DRAGONNET_COST, DRAGON_MOYEN_COST, DRAGON_GEANT_COST
from src.enum.type_entities import TypeEntitiesEnum
from src.player import Player

SPRITE_OPACITY = 150


class Dragon(Entity):

    def __init__(self, x_cell: int, y_cell: int, name: str, type_entity: List[TypeEntitiesEnum], max_hp: int,
                 attack_range: int, sprite_path: str,
                 speed: int,
                 attack_damage: int,
                 cost: int, player: Player, kill_reward: int = 0):
        super().__init__(x_cell, y_cell, name, type_entity, max_hp, attack_damage, attack_range, sprite_path,
                         kill_reward)
        self._speed_base: int = speed  # speed de base du dragon
        self._actual_speed: int = speed  # speed actuel du dragon
        self._speed_modifier: int = 0  # nombre de speed en plus ou en moins à celui de base
        self._cost: int = cost
        self._index_img: int = 0
        self._moving: bool = False
        self._target_cell: Cell | None = None
        self._anim_counter = 0
        self._type: List[TypeEntitiesEnum] = [TypeEntitiesEnum.DRAGON]
        self._player: Player = player
        self._has_moved: bool = False
        self._has_attacked: bool = False
        self._fireball = None

        if self._player:
            self.sprite_path = sprite_path.replace("bleu", self._player._color)

        self._sprite_sheet = pygame.image.load(self._sprite_path)
        self._imageSprite = [self._sprite_sheet.subsurface(x * 64, 0, 64, 64) for x in range(4)]

        self.path = []

    def reset_speed(self):
        """Réinitialise la vitesse à sa valeur de base."""
        self._actual_speed = self._speed_base
        self._speed_modifier = 0

    def reset_actions(self):
        """Réinitialise les drapeaux d'action du dragon pour le nouveau tour."""
        self._has_moved = False
        self._has_attacked = False

    def _check_purse_collection(self) -> int | None:
        """
        Vérifie si le dragon s'est arrêté sur une bourse, et la collecte si tel est le cas
        :return: Montant d'or collecté ou None
        """
        if not self.cell or not self._player:
            return

        # cherche si une bourse est présente dans la cellule
        purse = None
        for occupant in self.cell.occupants:
            if TypeEntitiesEnum.PLAYER_EFFECT_ZONE in occupant.type_entity:
                purse = occupant
                break

        if purse:
            # Ajoute l'or au joueur propriétaire du dragon
            amount = purse.amount
            self._player.economy.earn_gold(amount)
            sound.play("coin_pickup.wav")  # ramassage de bourse

            print(
                f"{self._player.name} a collecté une bourse de {amount} gold ! Total : {self._player.economy.get_gold()}")

            # Supprime la bourse de la grille
            self.cell.remove_occupant(purse)
            purse.destroy()
            return amount
        return None

    def attack_fireball(self, target: Entity):
        """
        Lance une boule de feu vers une cellule cible.
        :param target:
        """
        self._fireball = Fireball(self, target)

    def move_dragon(self, target_x: int, target_y: int, grid: Grid):
        self._target_cell = grid.cells[target_y][target_x]
        self._moving = True

        print(f"Déplacement du dragon {self.name} vers la cellule ({target_x}, {target_y})")
        self.path = find_path(grid, self.cell, self._target_cell)
        if self.path:
            print("Chemin trouvé :", self.path)
            print("Proprietaire du dragon : ", self._player.name)
            sound.play_loop("wing_flap.wav", identifier=f"dragon_move_{id(self)}")
        else:
            print("Pas de chemin possible")

    def update(self) -> int | None:
        """
        Met à jour la position du dragon lors de son déplacement
        :return: Montant d'or collecté ou None
        """

        if self._fireball:
            is_active = self._fireball.update()
            if not is_active:
                self._fireball = None

        if not self._moving or not self.path:
            return

        # La prochaine cellule cible
        target_cell = self.path[0]

        current_px = self.pixel_pos
        target_px = Position(
            target_cell.position.x * sc.TILE_SIZE + sc.OFFSET_X,
            target_cell.position.y * sc.TILE_SIZE + sc.OFFSET_Y
        )

        dx = target_px.x - current_px.x
        dy = target_px.y - current_px.y

        moved = False

        # Mouvement horizontal
        if dx != 0:
            moved = True
            direction = 1 if dx > 0 else -1
            current_px.x += min(self._actual_speed * 0.5, abs(dx)) * direction
            self.update_direction("droite" if direction > 0 else "gauche")

        # Mouvement vertical
        elif dy != 0:
            moved = True
            direction = 1 if dy > 0 else -1
            current_px.y += min(self._actual_speed * 0.5, abs(dy)) * direction

        if not moved or (dx == 0 and dy == 0):
            self.cell = target_cell
            self.path.pop(0)
            if not self.path:
                self._moving = False
                self._target_cell = None
                self._index_img = 0
                sound.stop(f"dragon_move_{id(self)}")
                # Vérifier si le dragon s'est arrêté sur une bourse
                amount = self._check_purse_collection()
                if amount:
                    return amount

        self._anim_counter += 1
        if self._anim_counter >= 10:
            self._anim_counter = 0
            self._index_img = (self._index_img + 1) % len(self._imageSprite)
        return None

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
        current_sprite = self._imageSprite[self._index_img]

        if self._has_moved and self._has_attacked:
            grayscale_sprite = pygame.transform.grayscale(current_sprite)
            grayscale_sprite.set_alpha(SPRITE_OPACITY)
            current_sprite = current_sprite.copy()
            current_sprite.blit(grayscale_sprite, (0, 0))

        target_size = int(sc.TILE_SIZE)
        scaled_sprite = pygame.transform.smoothscale(current_sprite, (target_size, target_size))

        x = self._pixel_pos.x + (sc.TILE_SIZE - target_size) // 2
        y = self._pixel_pos.y + (sc.TILE_SIZE - target_size) // 2

        surface.blit(scaled_sprite, (x, y))

        self.draw_health_bar(surface)

        if self._fireball:
            self._fireball.draw(surface)

    # ------- Getters et Setters -------
    @property
    def speed_base(self) -> int:
        return self._speed_base

    @speed_base.setter
    def speed_base(self, value: int) -> None:
        self._speed_base = value

    @property
    def actual_speed(self) -> int:
        return self._actual_speed

    @actual_speed.setter
    def actual_speed(self, value: int) -> None:
        self._actual_speed = value

    @property
    def speed_modifier(self) -> int:
        return self._speed_modifier

    @speed_modifier.setter
    def speed_modifier(self, value: int) -> None:
        self._speed_modifier = value

    @property
    def attack_damage(self) -> int:
        return self._attack_damage

    @attack_damage.setter
    def attack_damage(self, value: int) -> None:
        self._attack_damage = value

    @property
    def attack_range(self) -> int:
        return self._attack_range

    @attack_range.setter
    def attack_range(self, value: int) -> None:
        self._attack_range = value

    @property
    def cost(self) -> int:
        return self._cost

    @cost.setter
    def cost(self, value: int) -> None:
        self._cost = value

    @property
    def movement_points(self) -> int:
        return self._movement_points

    @movement_points.setter
    def movement_points(self, value: int) -> None:
        self._movement_points = value

    @property
    def moving(self) -> bool:
        return self._moving

    @moving.setter
    def moving(self, value: bool) -> None:
        self._moving = value

    @property
    def target_place(self) -> Position | None:
        return self._target_place

    @target_place.setter
    def target_place(self, value: Position | None) -> None:
        self._target_place = value

    @property
    def index_img(self) -> int:
        return self._index_img

    @index_img.setter
    def index_img(self, value: int) -> None:
        self._index_img = value

    @property
    def image_sprite(self) -> list:
        return self._imageSprite

    @image_sprite.setter
    def image_sprite(self, value: list) -> None:
        self._imageSprite = value

    @property
    def player(self) -> Player:
        return self._player

    @property
    def has_moved(self) -> bool:
        return self._has_moved

    @has_moved.setter
    def has_moved(self, value: bool) -> None:
        self._has_moved = value

    @property
    def has_attacked(self) -> bool:
        return self._has_attacked

    @has_attacked.setter
    def has_attacked(self, value: bool) -> None:
        self._has_attacked = value

    @property
    def fireball(self):
        return self._fireball

    def __str__(self):
        return (
            f"Dragon(name={self._name}, "
            f"HP={self._hp}/{self._max_hp}, "
            f"Attack={self._attack_damage}, "
            f"Range={self._attack_range}, "
            f"Speed={self._actual_speed}, "
            f"Cost={self._cost}, "
            f"Cell=({self.cell.position.x}, {self.cell.position.y}), "
            f"Moving={self._moving})"
        )


class Dragonnet(Dragon):
    """Classe représentant un dragonnet."""

    def __init__(self, x: int, y: int, player: Player = None):
        super().__init__(x, y, name="Dragonnet",
                         type_entity=[TypeEntitiesEnum.DRAGONNET, TypeEntitiesEnum.DRAGON, TypeEntitiesEnum.OBSTACLE],
                         max_hp=50, attack_range=1,
                         sprite_path="src/assets/sprites/dragonnet/dragonnet_bleu_droite.png",
                         speed=6, attack_damage=10, cost=DRAGONNET_COST, player=player, kill_reward=20)

    def draw(self, surface) -> None:
        """
        Affichage du dragonnet
        :param surface: Surface sur laquelle le dragonnet est placé
        :return: None
        """
        sprite = self._imageSprite[self._index_img]

        if self._has_moved and self._has_attacked:
            grayscale_sprite = pygame.transform.grayscale(sprite)
            grayscale_sprite.set_alpha(SPRITE_OPACITY)
            sprite = sprite.copy()
            sprite.blit(grayscale_sprite, (0, 0))

        target_size = int(sc.TILE_SIZE * 1.1)

        scaled_sprite = pygame.transform.smoothscale(sprite, (target_size, target_size))

        x = self._pixel_pos.x + (sc.TILE_SIZE - target_size) // 2
        y = self._pixel_pos.y + (sc.TILE_SIZE - target_size) // 2

        surface.blit(scaled_sprite, (x, y))
        self.draw_health_bar(surface)
        if self.fireball:
            self.fireball.draw(surface)


class DragonMoyen(Dragon):
    """Classe représentant un dragon moyen."""

    def __init__(self, x: int, y: int, player: Player = None):
        super().__init__(x, y, name="Dragon", type_entity=[TypeEntitiesEnum.DRAGON_MOYEN, TypeEntitiesEnum.DRAGON,
                                                           TypeEntitiesEnum.OBSTACLE],
                         max_hp=120, attack_range=2,
                         sprite_path="src/assets/sprites/dragon_moyen/dragon_moyen_bleu_droite.png",
                         speed=4, attack_damage=20, cost=DRAGON_MOYEN_COST, player=player, kill_reward=50)

    def draw(self, surface) -> None:
        """
        Affichage du dragon moyen
        :param surface: Surface sur laquelle le dragon est placé
        :return: None
        """
        sprite = self._imageSprite[self._index_img]

        if self._has_moved and self._has_attacked:
            grayscale_sprite = pygame.transform.grayscale(sprite)
            grayscale_sprite.set_alpha(SPRITE_OPACITY)
            sprite = sprite.copy()
            sprite.blit(grayscale_sprite, (0, 0))

        target_size = int(sc.TILE_SIZE * 1.4)

        scaled_sprite = pygame.transform.smoothscale(sprite, (target_size, target_size))

        x = self._pixel_pos.x + (sc.TILE_SIZE - target_size) // 2
        y = self._pixel_pos.y + (sc.TILE_SIZE - target_size) // 2

        surface.blit(scaled_sprite, (x, y))
        self.draw_health_bar(surface)
        if self.fireball:
            self.fireball.draw(surface)


class DragonGeant(Dragon):
    """Classe représentant un dragon géant."""

    def __init__(self, x: int, y: int, player: Player = None):
        super().__init__(x, y, name="Dragon Géant",
                         type_entity=[TypeEntitiesEnum.DRAGON_GEANT, TypeEntitiesEnum.DRAGON,
                                      TypeEntitiesEnum.OBSTACLE], max_hp=250,
                         attack_range=3,
                         sprite_path="src/assets/sprites/dragon_geant/dragon_geant_bleu_droite.png",
                         speed=2, attack_damage=40, cost=DRAGON_GEANT_COST, player=player, kill_reward=75)

    def draw(self, surface) -> None:
        """
        Affichage du dragon géant
        :param surface: Surface sur laquelle le dragon est placé
        :return: None
        """
        sprite = self._imageSprite[self._index_img]

        if self._has_moved and self._has_attacked:
            grayscale_sprite = pygame.transform.grayscale(sprite)
            grayscale_sprite.set_alpha(SPRITE_OPACITY)
            sprite = sprite.copy()
            sprite.blit(grayscale_sprite, (0, 0))

        target_size = int(sc.TILE_SIZE * 1.6)

        scaled_sprite = pygame.transform.smoothscale(sprite, (target_size, target_size))

        x = self._pixel_pos.x + (sc.TILE_SIZE - target_size) // 2
        y = self._pixel_pos.y + (sc.TILE_SIZE - target_size) // 2

        surface.blit(scaled_sprite, (x, y))
        self.draw_health_bar(surface)
        if self.fireball:
            self.fireball.draw(surface)


if __name__ == '__main__':
    # Création des dragons
    player = Player()
    d1 = Dragonnet(0, 0, player=player)
    d2 = DragonMoyen(5, 10, player=player)
    d3 = DragonGeant(12, 3, player=player)

    print("=== TEST DRAGONS ===")
    print(f"Dragonnet -> Pos: {d1.position}, HP: {d1.hp}, Speed: {d1.speed}, Cost: {d1.cost}, Sprite: {d1.sprite_path}")
    print(
        f"Dragon Moyen -> Pos: {d2.position}, HP: {d2.hp}, Speed: {d2.speed}, Cost: {d2.cost}, Sprite: {d2.sprite_path}")
    print(
        f"Dragon Géant -> Pos: {d3.position}, HP: {d3.hp}, Speed: {d3.speed}, Cost: {d3.cost}, Sprite: {d3.sprite_path}")
