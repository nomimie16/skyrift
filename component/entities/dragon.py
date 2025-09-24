from component.entities.entity import Entity

class Dragon(Entity):

    def __init__(self, x : int , y: int, max_hp: int, attack_range: int, sprite_path : str, speed: int, attack_damage: int, cost: int):
        super().__init__(x, y, max_hp, sprite_path)
        self.speed : int= speed
        self.attack_damage : int = attack_damage
        self.attack_range : int = attack_range
        self.cost : int = cost
        self.movement_points: int = speed

    def draw(self, surface):
        surface.blit(self.sprite, (self.position.x, self.position.y))

    def __str__(self):
        return super().__str__()


class Dragonnet(Dragon):
    def __init__(self, x,y):
        super().__init__(x,y, max_hp=50, attack_range=1, sprite_path="assets/sprites/dragonnet.png",
                         speed=6, attack_damage=10, cost=100)

class DragonMoyen(Dragon):
    def __init__(self, x,y):
        super().__init__(x,y, max_hp=120, attack_range = 2,sprite_path="assets/sprites/dragon.png",
                         speed=4, attack_damage=20, cost=300)

class DragonGeant(Dragon):
    def __init__(self, x,y):
        super().__init__(x,y, max_hp=250, attack_range = 3, sprite_path="assets/sprites/dragon_geant.png",
                         speed=2, attack_damage=40, cost=600)


if __name__ == '__main__':

    # Création des dragons
    d1 = Dragonnet(0,0)
    d2 = DragonMoyen(5, 10)
    d3 = DragonGeant(12, 3)

    print("=== TEST DRAGONS ===")
    print(f"Dragonnet -> Pos: {d1.position}, HP: {d1.hp}, Speed: {d1.speed}, Cost: {d1.cost}, Sprite: {d1.sprite_path}")
    print(f"Dragon Moyen -> Pos: {d2.position}, HP: {d2.hp}, Speed: {d2.speed}, Cost: {d2.cost}, Sprite: {d2.sprite_path}")
    print(f"Dragon Géant -> Pos: {d3.position}, HP: {d3.hp}, Speed: {d3.speed}, Cost: {d3.cost}, Sprite: {d3.sprite_path}")

