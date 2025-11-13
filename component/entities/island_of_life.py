from component.entities.entity import Entity
from component.entities.static_entity import StaticEntity


class IslandOfLife(StaticEntity):
    def __init__(self, x, y):
        super().__init__(x, y, name="Île de Vie", sprite_path="assets/sprites/life_island.png", width=4, height=4)

    def heal(self, entity: Entity):
        """Soigne une entité si elle se trouve sur l'île
        @:param entity: entité présente sur l'île
        """
        if self.rect.collidepoint(entity.position.x, entity.position.y):
            entity.hp += 2
