import pytest

from ...component import position

class TestPosition:
    
    def setup_method(self):
        """Initialisation précédant chaque test effectué"""
        self.position = position.Position(0, 0)

    def test_initial_position(self):
        """Test de la position initiale"""
        assert self.position.get_x() == 0
        assert self.position.get_y() == 0

    def test_move(self):
        """Test du déplacement"""
        self.position.move(2, -3)
        assert self.position.get_x() == 2
        assert self.position.get_y() == -3

        self.position.move(-2, 3)
        assert self.position.get_x() == 0
        assert self.position.get_y() == 0