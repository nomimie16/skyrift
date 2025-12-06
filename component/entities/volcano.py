from component.entities.volcano_effect import VolcanoEffect
from component.entities.zone_entity import ZoneEntity
from component.enum.type_entities import TypeEntitiesEnum


class Volcano(ZoneEntity):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x, y=y,
            sprite_path="assets/img/volcano.png",
            width=8, height=8,
            zone_effect=VolcanoEffect()
        )
        self.name = "Volcan"
        self.type_entity.append(TypeEntitiesEnum.VOLCANO)
