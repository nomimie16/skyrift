import pytest
from component.entities.dragon import Dragonnet
from component.position import Position
from grid import Grid

class TestGrid:
    
    def setup_method_grid(self):
        """Initialisation précédant chaque test effectué"""
        self.grid = Grid(5,5)  
    
    
    def setup_methode_pos(self):
        """Initialisation précédant chaque test effectué"""
        self.position = Position(0,0) 
    
    def test_add_occupant(self):
        """Test de l'ajout d'un occupant dans une cellule"""
        pos = Position(2, 3)
        occupant = Dragonnet(1, 1)
        result = self.grid.add_occupant(occupant, pos)
        assert result == True
        assert self.grid.cells[3][2].get_occupant() == occupant
