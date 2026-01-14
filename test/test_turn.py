from src.const import MAX_MOVES_PER_TURN, MAX_ATTACKS_PER_TURN
from src.player import Player
from src.turn import Turn

#Classe pour tester les fonctionnalités de la classe Turn
class TestTurn:
    
    def setup_method(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.turn = Turn(self.player1, self.player2)
    def test_initial_state(self):
        assert self.turn.current_player() == self.player1
        assert self.turn.get_turn_number() == 0
        assert self.turn.can_move() is True
        assert self.turn.can_attack() is True
    def test_next_turn(self):
        self.turn.next()
        assert self.turn.current_player() == self.player2
        assert self.turn.get_turn_number() == 1
        self.turn.next()
        assert self.turn.current_player() == self.player1
        assert self.turn.get_turn_number() == 2
        
    def test_move_and_attack_limits(self):
        for _ in range(MAX_MOVES_PER_TURN):
            assert self.turn.can_move() is True
            self.turn.use_move()
        assert self.turn.can_move() is False
        
        for _ in range(MAX_ATTACKS_PER_TURN):
            assert self.turn.can_attack() is True
            self.turn.use_attack()
        assert self.turn.can_attack() is False
    def test_counters_reset_on_next(self):  
        for _ in range(MAX_MOVES_PER_TURN):
            self.turn.use_move()
        for _ in range(MAX_ATTACKS_PER_TURN):
            self.turn.use_attack()
        self.turn.next()
        assert self.turn.can_move() is True
        assert self.turn.can_attack() is True
    