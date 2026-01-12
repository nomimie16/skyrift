from src.component.entities.entity import Entity


class EffectZone:
    """
    Classe de base pour les zones d'effet.
    """

    def apply_effect(self, entity: Entity) -> None:
        """Applique l'effet à l'entité donnée.
        :param: entity (Entity): L'entité à affecter.
        :return: None"""
        pass

    def remove_effect(self, entity: Entity) -> None:
        """Retire l'effet à l'entité donnée.
        :param: entity (Entity): L'entité à affecter.
        :return: None"""
        pass
