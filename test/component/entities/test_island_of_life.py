from component.entities.island_of_life import IslandOfLife
from component.entities.entity import Entity
from unittest.mock import patch

class TestIslandOfLife:

    def setup_method(self):
        with patch('pygame.image.load'):
            self.island = IslandOfLife(1, 1)
            self.entity = Entity(1, 1, "test", 10, "assets/sprites/dragonnet.png")

    def test_heal(self):
        self.entity.hp = 2
        self.island.heal(self.entity)
        assert self.entity.hp == 4
