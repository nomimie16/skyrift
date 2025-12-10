from component.entities.entity import Entity
from component.entities.static_entity import StaticEntity
from component.enum.type_entities import TypeEntitiesEnum


class IslandOfLife(StaticEntity):
    def __init__(self, x, y):
        super().__init__(x, y, name="Île de Vie",
                         type_entity=[TypeEntitiesEnum.ISLAND_OF_LIFE, TypeEntitiesEnum.EFFECT_ZONE],
                         sprite_path="assets/img/ile_de_vie.png", width=4, height=4)

    def heal(self, entity: Entity):
        """Soigne une entité si elle se trouve sur l'île
        @:param entity: entité présente sur l'île
        """
        if self.rect.collidepoint(entity.position.x, entity.position.y):
            entity.hp += 2
