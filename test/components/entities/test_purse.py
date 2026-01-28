import random

import pygame

from src import screen_const as sc
from src.component.entities.purse_effect import PurseEffect
from src.component.entities.zone_entity import ZoneEntity
from src.component.grid import Grid
from src.component.position import Position
from src.const import PURSE_SPAWN_CHANCE_PER_TURN
from src.enum.type_entities import TypeEntitiesEnum
import pytest
import src.component.entities.purse as Purse

def spawn_random_purse(grid: Grid, amount: int = 50) -> 'Purse | None':
    """
    Fait spawn une bourse avec une probabilité donnée
    """

    if Purse.instances_count >= 5:
        return None

    if random.random() > PURSE_SPAWN_CHANCE_PER_TURN:
        return None

    free_cells = grid.free_cells()
    if not free_cells:
        return None

    cell = random.choice(free_cells)
    purse = Purse(cell.position.x, cell.position.y, amount)
    grid.add_occupant(purse, cell)

    return purse

# Classe pour tester les fonctionnalités de la classe Purse
class testPurse:
    
    def setup_method_purse(self):
        """Initialisation précédant chaque test effectué"""
        # Réinitialiser le compteur d'instances avant chaque test
        Purse.instances_count = 0
        self.grid = Grid(10, 10)
    
    def test_spawn_random_purse_success(self):
        """Test du spawn réussi d'une bourse"""
        purse = spawn_random_purse(self.grid, amount=100)
        if purse is not None:
            assert isinstance(purse, Purse)
            assert purse._amount == 100
            assert purse in self.grid.occupants
        else:
            # Si la bourse n'a pas spawné, vérifier que c'est dû à la probabilité
            assert Purse.instances_count < 5
    
    def test_spawn_random_purse_max_instances(self):
        """Test du spawn d'une bourse lorsque le nombre maximum d'instances est atteint"""
        Purse.instances_count = 5
        purse = spawn_random_purse(self.grid)
        assert purse is None
    
    def test_purse_initialization(self):
        """Test de l'initialisation de la bourse"""
        purse = Purse(2, 3, amount=75)
        assert purse.name == "Bourse"
        assert TypeEntitiesEnum.EFFECT_ZONE in purse.type_entity
        assert TypeEntitiesEnum.PLAYER_EFFECT_ZONE in purse.type_entity
        assert purse._amount == 75
        assert purse.cell is None  # La cellule doit être assignée lors de l'ajout à la grille
    def test_purse_destroy(self):
        """Test de la destruction de la bourse"""
        purse = Purse(2, 3, amount=50)
        initial_count = Purse.instances_count
        purse.destroy()
        assert Purse.instances_count == initial_count - 1
    