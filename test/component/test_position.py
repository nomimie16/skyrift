import unittest

from component.position import Position


class TestPosition(unittest.TestCase):

    def setUp(self):
        """Initialise des positions pour chaque test"""
        self.pos1 = Position(0, 0)
        self.pos2 = Position(5, 10)
        self.pos3 = Position(12, 3)

    def test_initialisation(self):
        """Test que les coordonnées initiales sont correctes"""
        self.assertEqual(self.pos1.get_x(), 0)
        self.assertEqual(self.pos1.get_y(), 0)
        self.assertEqual(self.pos2.get_x(), 5)
        self.assertEqual(self.pos2.get_y(), 10)
        self.assertEqual(self.pos3.get_x(), 12)
        self.assertEqual(self.pos3.get_y(), 3)

    def test_move_positive(self):
        """Test le déplacement avec des valeurs positives"""
        self.pos2.move(3, 2)
        self.assertEqual(self.pos2.get_x(), 8)
        self.assertEqual(self.pos2.get_y(), 12)

    def test_move_negative(self):
        """Test le déplacement avec des valeurs négatives"""
        self.pos3.move(-12, 2)
        self.assertEqual(self.pos3.get_x(), 0)
        self.assertEqual(self.pos3.get_y(), 5)

    def test_str(self):
        """Test l'affichage de la position"""
        self.assertEqual(str(self.pos1), "(0, 0)")
        self.pos1.move(2, 3)
        self.assertEqual(str(self.pos1), "(2, 3)")


if __name__ == '__main__':
    unittest.main()
