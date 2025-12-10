from component.entities.entity import Entity
from component.entities.static_entity import StaticEntity
from component.enum.type_entities import TypeEntitiesEnum


class Volcano(StaticEntity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, name="Volcan", type_entity=[TypeEntitiesEnum.VOLCANO, TypeEntitiesEnum.OBSTACLE],
                         sprite_path="assets/img/volcano.png", width=8, height=8)

    def apply_effect(self, entity: Entity):
        """
        Ajoute un effet de perte de vitesse et de vie au dragon
        :param entity:
        :return:
        """
        if self.rect.collidepoint(entity.position.x, entity.position.y):
            entity.hp -= 2
            entity.speed_modifier = -1
            entity.movement_points = max(0, entity.base_speed + entity.speed_modifier)
        else:
            entity.reset_speed()
