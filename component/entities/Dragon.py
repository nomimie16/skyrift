from component.Position import Position

class Dragon:

    def __init__(self, position : Position, hp, attack_damage, speed, cost, sprite_path):
        self.position = position
        self.hp = hp
        self.speed = speed
        self.cost = cost
        self.sprite_path = sprite_path

    def draw(self, surface):
        pass

    def __str__(self):
        return super().__str__()


class Dragonnet(Dragon):
    def __init__(self, position):
        super().__init__(position, hp=50, sprite_path="assets/sprites/dragonnet.png",
                         speed=6, attack_damage=10, cost=100)

class DragonMoyen(Dragon):
    def __init__(self, position):
        super().__init__(position, hp=120, sprite_path="assets/sprites/dragon.png",
                         speed=4, attack_damage=20, cost=300)

class DragonGeant(Dragon):
    def __init__(self, position):
        super().__init__(position, hp=250, sprite_path="assets/sprites/dragon_geant.png",
                         speed=2, attack_damage=40, cost=600)


if __name__ == '__main__':

    # Création de positions
    pos1 = Position(0, 0)
    pos2 = Position(5, 10)
    pos3 = Position(12, 3)

    # Création des dragons
    d1 = Dragonnet(pos1)
    d2 = DragonMoyen(pos2)
    d3 = DragonGeant(pos3)

    print("=== TEST DRAGONS ===")
    print(f"Dragonnet -> Pos: {d1.position}, HP: {d1.hp}, Speed: {d1.speed}, Cost: {d1.cost}, Sprite: {d1.sprite_path}")
    print(f"Dragon Moyen -> Pos: {d2.position}, HP: {d2.hp}, Speed: {d2.speed}, Cost: {d2.cost}, Sprite: {d2.sprite_path}")
    print(f"Dragon Géant -> Pos: {d3.position}, HP: {d3.hp}, Speed: {d3.speed}, Cost: {d3.cost}, Sprite: {d3.sprite_path}")

