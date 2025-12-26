from component.entities.effect_zone import EffectZone
from component.entities.static_entity import StaticEntity
from component.enum.type_entities import TypeEntitiesEnum


class ZoneEntity(StaticEntity):
    """
    Entité statique qui possède un effet de zone.
    Elle s'étend sur une ou plusieurs cellules.
    """

    def __init__(self, x: int, y: int, sprite_path: str | None, width: int, height: int,
                 type_entity: list[TypeEntitiesEnum],
                 zone_effect: EffectZone):
        super().__init__(x, y, name="Zone", type_entity=type_entity,
                         sprite_path=sprite_path, width=width, height=height)
        self._zone_effect = zone_effect

    @property
    def effect(self) -> EffectZone:
        """
        Retourne l'effet de zone associé à cette entité.
        :return: EffectZone
        """
        return self._zone_effect
