from src.component.entities.island_of_life_effect import IslandOfLifeEffect
from src.component.entities.zone_entity import ZoneEntity
from src.enum.type_entities import TypeEntitiesEnum


class IslandOfLife(ZoneEntity):
    """
    Île de vie : zone qui soigne les entités qui y entrent.
    """

    def __init__(self, x, y):
        super().__init__(x, y, sprite_path="src/assets/img/ile_de_vie.png", width=4, height=4,
                         type_entity=[TypeEntitiesEnum.EFFECT_ZONE, TypeEntitiesEnum.GOOD_EFFECT_ZONE,
                                      TypeEntitiesEnum.ISLAND_OF_LIFE],
                         zone_effect=IslandOfLifeEffect())
        self.name = "Île de vie"
