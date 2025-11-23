from component.entities.entity import Entity


class Base(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, name="Base", max_hp=2000, attack_damage=0, attack_range=0,
                         sprite_path="assets/sprites/base.png")
