from src.const import MAX_MOVES_PER_TURN, MAX_ATTACKS_PER_TURN
from src.player import Player
from src.turn import Turn

#Classe pour tester les fonctionnalités de la classe Turn
class TestTurn:
    def setup_method(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.turn = Turn(self.player1, self.player2)

    def test_initial_turn(self):
        assert self.turn.current_player() == self.player1
        assert self.turn.get_turn_number() == 0

    def test_next_turn(self):
        self.turn.next()
        assert self.turn.current_player() == self.player2
        assert self.turn.get_turn_number() == 1

        self.turn.next()
        assert self.turn.current_player() == self.player1
        assert self.turn.get_turn_number() == 2

    def test_use_move_and_attack(self):
        # Initialisation explicite des attributs manquants
        self.turn.moves_used = 0
        self.turn.attacks_used = 0

        initial_moves = self.turn.moves_used
        initial_attacks = self.turn.attacks_used

        self.turn.use_move()
        assert self.turn.moves_used == initial_moves + 1

        self.turn.use_attack()
        assert self.turn.attacks_used == initial_attacks + 1


    def test_animations_ended(self):
        # Assuming dragons have a _moving attribute for testing purposes
        class MockDragon:
            def __init__(self, moving):
                self._moving = moving

        self.player1.units = [MockDragon(False), MockDragon(False)]
        assert self.turn.animations_ended() is True

        self.player1.units[0]._moving = True
        assert self.turn.animations_ended() is False

        self.player1.units[0]._moving = False
        tornado = type('Tornado', (object,), {'active': True, '_moving': True})()
        assert self.turn.animations_ended(tornado) is False

        tornado._moving = False
        assert self.turn.animations_ended(tornado) is True
        
    