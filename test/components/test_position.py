import pytest

from ... import position

class TestPosition:
    
    def steup_method(self):
        """Initialisation précédant chaque test effectué"""
        self.position = position.Position(0, 0)

    def test_initial_position(self):
        """Test de la position initiale"""
        assert self.position.get_coordinates() == (0, 0)

    def test_move(self):
        """Test du déplacement"""
        self.position.move(2, -3)
        assert self.position.get_coordinates() == (2, -3)
        self.posistion.move(-2, 3)
        assert self.position.get_coordinates() == (0, 0)