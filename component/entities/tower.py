from component.entities.entity import Entity


class Tower(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, max_hp=300, sprite_path="assets/sprites/tour.png")
        self._attack_damage = 25
        self._attack_range = 3
