from component.entities.entity import Entity

class Base(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, max_hp=2000, sprite_path="assets/sprites/base.png")
