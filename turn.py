from player import Player

class Turn:
    def __init__(self, p1, p2):
        self.p1: Player = p1
        self.p2: Player = p2
        self.turn: Player = p1
        self.count: int = 0
    
    def next(self):
        self.count += 1
        if self.turn == self.p1:
            self.turn = self.p2
        else:
            self.turn = self.p1

    def current_player(self) -> Player:
        return self.turn
    
    def get_turn_number(self) -> int:
        return self.count