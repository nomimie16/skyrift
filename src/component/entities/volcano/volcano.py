from src.component.entities.static_entity import StaticEntity
from src.enum.type_entities import TypeEntitiesEnum
from .volcano_effect_zone import VolcanoEffectZone
from .volcano_obstacle_zone import VolcanoObstacle


class Volcano(StaticEntity):
    """
    Volcan complet
    """

    def __init__(self, x: int, y: int):
        super().__init__(
            x_cell=x,
            y_cell=y,
            name="Volcano",
            sprite_path="src/assets/img/volcan_explosion.png",
            width=8,
            height=8,
            type_entity=[TypeEntitiesEnum.VOLCANO]
        )

        self.obstacle = VolcanoObstacle(x, y)
        self.effect_zone = VolcanoEffectZone(x, y)
