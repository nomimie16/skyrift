from src.const import MAX_MOVES_PER_TURN, MAX_ATTACKS_PER_TURN
from src.player import Player


class Turn:
    def __init__(self, p1, p2):
        self.p1: Player = p1
        self.p2: Player = p2
        self.turn: Player = p1
        self.count: int = 0

    def next(self):
        for dragon in self.turn.units:
            dragon.reset_actions()
        self.count += 1
        if self.turn == self.p1:
            self.turn = self.p2
        else:
            self.turn = self.p1

    def current_player(self) -> Player:
        return self.turn

    def get_turn_number(self) -> int:
        return self.count

    def use_move(self):
        """Marque qu'un dragon a été déplacé ce tour"""
        self.moves_used += 1

    def use_attack(self):
        """Marque qu'une attaque a été effectuée ce tour"""
        self.attacks_used += 1

    def animations_ended(self, tornado=None) -> bool:
        """
        Vérifie si tous les dragons du joueur actuel ainsi que la tornade ont terminé leurs animations
        """
        for dragon in self.turn.units:
            if dragon._moving:
                return False
        
        if tornado and tornado.active and tornado._moving:
            return False
        
        return True
