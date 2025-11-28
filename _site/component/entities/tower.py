from component.entities.entity import Entity


class Tower(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, name="Tour de défense", max_hp=300, sprite_path="assets/sprites/tour.png")
        self._attack_damage: int = 25
        self._attack_range: int = 3

    # ------- Getters et Setters -------

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
