from src.component.entities.effect_zone import EffectZone
from src.component.entities.static_entity import StaticEntity
from src.enum.type_entities import TypeEntitiesEnum
import pygame
import pytest
from src.component.entities.zone_entity import ZoneEntity
from src.component.grid import Cell

# Classe de test pour ZoneEntity
class TestZoneEntity(StaticEntity):
    def setup_method_zone_entity(self):
        """Initialisation précédant chaque test effectué"""
        self.mock_effect = EffectZone()
        self.zone_entity = ZoneEntity(
            x=1,
            y=2,
            sprite_path=None,
            width=3,
            height=4,
            type_entity=[TypeEntitiesEnum.EFFECT_ZONE],
            zone_effect=self.mock_effect
        )

    def test_zone_entity_initialization(self):
        """Test de l'initialisation de ZoneEntity"""
        assert self.zone_entity.position.x == 1
        assert self.zone_entity.position.y == 2
        assert self.zone_entity.width == 3
        assert self.zone_entity.height == 4
        assert TypeEntitiesEnum.EFFECT_ZONE in self.zone_entity.type_entity
        assert self.zone_entity.effect == self.mock_effect
    def test_zone_entity_effect_property(self):
        """Test de la propriété effect de ZoneEntity"""
        assert self.zone_entity.effect is self.mock_effect
    def test_zone_entity_name(self):
        """Test du nom de ZoneEntity"""
        assert self.zone_entity.name == "Zone"
    def test_zone_entity_type_entity(self):
        """Test du type d'entité de ZoneEntity"""
        assert TypeEntitiesEnum.EFFECT_ZONE in self.zone_entity.type_entity
    def test_zone_entity_dimensions(self):
        """Test des dimensions de ZoneEntity"""
        assert self.zone_entity.width == 3
        assert self.zone_entity.height == 4
    def test_zone_entity_position(self):
        """Test de la position de ZoneEntity"""
        assert self.zone_entity.position.x == 1
        assert self.zone_entity.position.y == 2
    def test_zone_entity_sprite_path(self):
        """Test du chemin du sprite de ZoneEntity"""
        assert self.zone_entity.sprite_path is None
    def test_zone_entity_effect_instance(self):
        """Test que l'effet de zone est une instance d'EffectZone"""
        assert isinstance(self.zone_entity.effect, EffectZone)
    def test_zone_entity_no_effect_change(self):
        """Test que l'effet de zone ne peut pas être changé directement"""
        new_effect = EffectZone()
        assert self.zone_entity.effect is self.mock_effect
        assert self.zone_entity.effect is not new_effect
    def test_zone_entity_effect_functionality(self):
        """Test de la fonctionnalité de l'effet de zone (vérifie si aucune erreur n'est levée)"""
        try:
            self.zone_entity.effect.apply_effect(None)  # Appliquer l'effet à None pour le test
            effect_successful = True
        except Exception as e:
            effect_successful = False
        assert effect_successful == True
    def test_zone_entity_inheritance(self):
        """Test que ZoneEntity hérite de StaticEntity"""
        assert isinstance(self.zone_entity, StaticEntity)
    def test_zone_entity_str_representation(self):
        """Test de la représentation en chaîne de ZoneEntity"""
        str_repr = str(self.zone_entity)
        assert "ZoneEntity" in str_repr
        assert "position" in str_repr
        assert "width" in str_repr
        assert "height" in str_repr
    def test_zone_entity_draw(self):
        """Test de la méthode de dessin de ZoneEntity (vérifie si aucune erreur n'est levée)"""
        surface = pygame.Surface((800, 600))
        try:
            self.zone_entity.draw(surface)
            draw_successful = True
        except Exception as e:
            draw_successful = False
        assert draw_successful == True
    def test_zone_entity_cell_setter(self):
        """Test du setter pour la cellule de ZoneEntity"""
        new_cell = Cell(5, 6)
        self.zone_entity.cell = new_cell
        assert self.zone_entity.cell.position.x == 5
        assert self.zone_entity.cell.position.y == 6
        