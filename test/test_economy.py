import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import economy

class TestEconomy(unittest.TestCase):
    
    def setUp(self):
        """Appelée avant chaque test"""
        self.economy = economy.Economy() # 100 PO de base
    
    def test_initial_gold(self):
        """Test de l'or initial"""
        self.assertEqual(self.economy.get_gold(), 100)
    
    def test_earn_gold(self):
        """Test d'ajout d'or"""
        self.economy.earn_gold(50)
        self.assertEqual(self.economy.get_gold(), 150)
    
    def test_spend_gold(self):
        """Test de dépense d'or"""
        self.economy.spend_gold(30)
        self.assertEqual(self.economy.get_gold(), 70)
    
    def test_can_afford(self):
        """Test de vérification du solde d'or"""
        self.assertTrue(self.economy.can_afford(50))
        self.assertFalse(self.economy.can_afford(200))
    
    def test_spend_too_much(self):
        """Test d'élévation d'erreur en cas de dépense supérieure au solde d'or"""
        with self.assertRaises(ValueError):
            self.economy.spend_gold(200)

if __name__ == "__main__":
    unittest.main()