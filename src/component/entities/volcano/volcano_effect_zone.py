from src.component.entities.zone_entity import ZoneEntity
from src.enum.type_entities import TypeEntitiesEnum
from .volcano_effect import VolcanoEffect


class VolcanoEffectZone(ZoneEntity):
    """
    Partie du volcan ayant un effet de zone
    """

    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            sprite_path=None,
            width=8,
            height=3,
            type_entity=[
                TypeEntitiesEnum.VOLCANO,
                TypeEntitiesEnum.EFFECT_ZONE,
                TypeEntitiesEnum.BAD_EFFECT_ZONE
            ],
            zone_effect=VolcanoEffect()
        )
        self.name = "VolcanoEffectZone"
