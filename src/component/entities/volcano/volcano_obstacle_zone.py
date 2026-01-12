from src.component.entities.static_entity import StaticEntity
from src.enum.type_entities import TypeEntitiesEnum


class VolcanoObstacle(StaticEntity):
    """
    Partie du volcan où on ne peut pas se déplacer
    """

    def __init__(self, x: int, y: int):
        super().__init__(
            x_cell=x,
            y_cell=y,
            name="VolcanoObstacle",
            sprite_path=None,
            width=8,
            height=5,
            type_entity=[TypeEntitiesEnum.OBSTACLE, TypeEntitiesEnum.VOLCANO]
        )
