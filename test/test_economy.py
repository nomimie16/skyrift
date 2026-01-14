import pytest

from src import economy

# Classe de test pour le module economy
class TestEconomy:
    def setup_method(self):
        self.econ = economy.Economy(initial_gold=500)

    def test_initial_gold(self):
        assert self.econ.get_gold() == 500

    def test_earn_gold(self):
        self.econ.earn_gold(200)
        assert self.econ.get_gold() == 700

    def test_spend_gold_success(self):
        self.econ.spend_gold(300)
        assert self.econ.get_gold() == 200

    def test_spend_gold_failure(self):
        with pytest.raises(ValueError):
            self.econ.spend_gold(600)

    def test_can_afford_true(self):
        assert self.econ.can_afford(400) is True

    def test_can_afford_false(self):
        assert self.econ.can_afford(600) is False

    def test_set_gold(self):
        self.econ.set_gold(800)
        assert self.econ.get_gold() == 800

    def test_listeners_notification(self):
        notifications = []

        def listener(delta):
            notifications.append(delta)

        self.econ.add_listener(listener)
        self.econ.earn_gold(100)
        self.econ.spend_gold(50)

        assert notifications == [100, -50]
    
    