from component.entities.entity import Entity
from component.enum.type_entities import TypeEntitiesEnum


class Base(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, name="Base", type_entity=[TypeEntitiesEnum.BASE, TypeEntitiesEnum.OBSTACLE], max_hp=2000,
                         attack_damage=0, attack_range=0,
                         sprite_path="assets/sprites/base.png")
