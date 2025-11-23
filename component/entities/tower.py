from component.entities.entity import Entity


class Tower(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, name="Tour de défense", max_hp=300, attack_damage=25, attack_range=3,
                         sprite_path="assets/sprites/tour.png")
