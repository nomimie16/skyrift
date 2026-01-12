import pytest

from src import economy


class TestEconomy:

    def setup_method(self):
        """Initialisation précédant chaque test effectué"""
        self.economy = economy.Economy()  # 100 PO de base

    def test_initial_gold(self):
        """Test de l'or initial"""
        assert self.economy.get_gold() == 100

    def test_earn_gold(self):
        """Test d'ajout d'or"""
        self.economy.earn_gold(50)
        assert self.economy.get_gold() == 150

    def test_spend_gold(self):
        """Test de dépense d'or"""
        self.economy.spend_gold(30)
        assert self.economy.get_gold() == 70

    def test_can_afford(self):
        """Test de vérification du solde d'or"""
        assert self.economy.can_afford(50) == True
        assert self.economy.can_afford(200) == False

    def test_spend_too_much(self):
        """Test d'élévation d'erreur en cas de dépense supérieure au solde d'or"""
        with pytest.raises(ValueError):
            self.economy.spend_gold(200)
