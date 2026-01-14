import pygame
import pytest
from src import screen_const as sc
from src.component.entities.entity import Entity
from src.enum.type_entities import TypeEntitiesEnum
from src.component.entities.base import Base

# Classe pour tester les fonctionnalités de la classe Base
class TestBase(Entity):
    
    def setup_method_base(self):
        """Initialisation précédant chaque test effectué"""
        self.base = Base(4, 4, sprite_path="path/to/sprite.png", player="Player 1")
    
    def test_base_initialization(self):
        """Test de l'initialisation de la base"""
        assert self.base.name == "Base"
        assert TypeEntitiesEnum.BASE in self.base.type_entity
        assert TypeEntitiesEnum.OBSTACLE in self.base.type_entity
        assert self.base.max_hp == 2000
        assert self.base.attack_damage == 0
        assert self.base.attack_range == 0
        assert self.base.width == 4
        assert self.base.height == 4
        assert self.base.player == "Player 1"
    
    def test_base_player_setter(self):
        """Test du setter pour le joueur de la base"""
        self.base.player = "Player 2"
        assert self.base.player == "Player 2"
    
    def test_base_draw(self):
        """Test de la méthode de dessin de la base (vérifie si aucune erreur n'est levée)"""
        surface = pygame.Surface((sc.SCREEN_WIDTH, sc.SCREEN_HEIGHT))
        try:
            self.base.draw(surface)
            draw_successful = True
        except Exception as e:
            draw_successful = False
        assert draw_successful == True
    
    