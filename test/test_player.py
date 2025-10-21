from .. import player

class TestPlayer:

    def setup_method(self):
        self.player = player.Player()

    def test_add_unit(self):
        self.player.add_unit(1)
        self.player.add_unit(3)
        assert self.player.units == [1, 3]

    def test_remove_unit(self):
        self.player.add_unit(1)
        self.player.add_unit(3)
        self.player.remove_unit(1)
        assert self.player.units == [1]
    