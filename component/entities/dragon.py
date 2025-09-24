import pygame

from component.entities.entity import Entity
from component.position import Position


class Dragon(Entity):

    def __init__(self, x: int, y: int, max_hp: int, attack_range: int, sprite_path: str, speed: int, attack_damage: int,
                 cost: int):
        super().__init__(x, y, max_hp, sprite_path)
        self._speed: int = speed
        self._attack_damage: int = attack_damage
        self._attack_range: int = attack_range
        self._cost: int = cost
        self._movement_points: int = speed
        self._index_img: int = 0
        self._moving: bool = False
        self._target_place: Position | None = None
        self._sprite_sheet = pygame.image.load(sprite_path)
        self._imageSprite = [self._sprite_sheet.subsurface(x * 64, 0, 64, 64) for x in range(4)]

    def move_dragon(self, x: int, y: int):
        """Définir une nouvelle cible"""
        self._target_place = Position(x, y)
        self._moving = True

    def update(self):
        if not self._moving or self._target_place:
            dx: int = self._target_place.x - self._position.x
            dy: int = self._target_place.y - self._position.y

        if dx != 0:
            step = 1 if dx > 0 else -1
            self._position.move(step, 0)
        elif dy != 0:
            step = 1 if dy > 0 else -1
            self._position.move(0, step)
        else:
            self._moving = False
            return

        self._index_img = (self._index_img + 1) % len(self._imageSprite)

    def draw(self, surface):
        surface.blit(self._imageSprite[self._index_img], (int(self._position.x), int(self._position.y)))

    def __str__(self):
        return super().__str__()


class Dragonnet(Dragon):
    def __init__(self, x, y):
        super().__init__(x, y, max_hp=50, attack_range=1, sprite_path="assets/sprites/dragonnet.png",
                         speed=6, attack_damage=10, cost=100)


class DragonMoyen(Dragon):
    def __init__(self, x, y):
        super().__init__(x, y, max_hp=120, attack_range=2, sprite_path="assets/sprites/dragon.png",
                         speed=4, attack_damage=20, cost=300)


class DragonGeant(Dragon):
    def __init__(self, x, y):
        super().__init__(x, y, max_hp=250, attack_range=3, sprite_path="assets/sprites/dragon_geant.png",
                         speed=2, attack_damage=40, cost=600)


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
