from component.entities.island_of_life_effect import IslandOfLifeEffect
from component.entities.zone_entity import ZoneEntity
from component.enum.type_entities import TypeEntitiesEnum


class IslandOfLife(ZoneEntity):
    def __init__(self, x, y):
        super().__init__(x, y, sprite_path="assets/img/ile_de_vie.png", width=4, height=4,
                         zone_effect=IslandOfLifeEffect())
        self.name = "Île de vie"
        self.type_entity = [TypeEntitiesEnum.ISLAND_OF_LIFE, TypeEntitiesEnum.EFFECT_ZONE]
