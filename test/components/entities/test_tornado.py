from random import randint

import pygame

from src import screen_const as sc
from src.component.entities.tornado_effect import TornadoEffect
from src.component.entities.zone_entity import ZoneEntity
from src.component.grid import Cell
from src.component.grid import Grid
from src.component.path_finding import find_path
from src.component.position import Position
from src.enum.type_entities import TypeEntitiesEnum
from unittest.mock import patch, MagicMock
from src.component.entities.tornado import Tornado

# Classe pour tester les fonctionnalités de la classe Tornado
class TestTornado(ZoneEntity):
    
    def setup_method_tornado(self):
        """Initialisation précédant chaque test effectué"""
        self.tornado = Tornado(2, 3)
    
    def test_tornado_initialization(self):
        """Test de l'initialisation de la tornade"""
        assert self.tornado._name == "Tornade"
        assert TypeEntitiesEnum.TORNADO in self.tornado.type_entity
        assert TypeEntitiesEnum.EFFECT_ZONE in self.tornado.type_entity
        assert TypeEntitiesEnum.BAD_EFFECT_ZONE in self.tornado.type_entity
        assert self.tornado.width == 2
        assert self.tornado.height == 3
        assert isinstance(self.tornado.zone_effect, TornadoEffect)
        assert 2 <= self.tornado._duration <= 10
    
    def test_tornado_handle_turn(self):
        """Test de la gestion d'un tour avec la tornade (vérifie si aucune erreur n'est levée)"""
        grid = Grid(10, 10)
        grid.add_occupant(self.tornado, self.tornado.cell)
        try:
            self.tornado.handle_turn(grid)
            handle_turn_successful = True
        except Exception as e:
            handle_turn_successful = False
        assert handle_turn_successful == True
    def test_tornado_move_tornado(self):
        """Test du déplacement de la tornade (vérifie si aucune erreur n'est levée)"""
        grid = Grid(10, 10)
        grid.add_occupant(self.tornado, self.tornado.cell)
        try:
            self.tornado.move_tornado(grid)
            move_successful = True
        except Exception as e:
            move_successful = False
        assert move_successful == True
    def test_tornado_disable_and_activate(self):
        """Test de la désactivation et de l'activation de la tornade (vérifie si aucune erreur n'est levée)"""
        grid = Grid(10, 10)
        grid.add_occupant(self.tornado, self.tornado.cell)
        try:
            self.tornado.tornado_disable(grid)
            self.tornado.tornado_activation(grid)
            toggle_successful = True
        except Exception as e:
            toggle_successful = False
        assert toggle_successful == True
    def test_tornado_duration_setter(self):
        """Test du setter pour la durée de la tornade"""
        initial_duration = self.tornado._duration
        self.tornado._duration = 5
        assert self.tornado._duration == 5
        assert self.tornado._duration != initial_duration
    def test_tornado_active_setter(self):
        """Test du setter pour l'état actif de la tornade"""
        initial_active = self.tornado._active
        self.tornado._active = False
        assert self.tornado._active == False
        assert self.tornado._active != initial_active
    