from player import Player
from const import MAX_MOVES_PER_TURN, MAX_ATTACKS_PER_TURN


class Turn:
    def __init__(self, p1, p2):
        self.p1: Player = p1
        self.p2: Player = p2
        self.turn: Player = p1
        self.count: int = 0
        self.moves_used: int = 0
        self.attacks_used: int = 0

    def next(self):
        self.count += 1
        if self.turn == self.p1:
            self.turn = self.p2
        else:
            self.turn = self.p1
        # Remettre les compteurs a zero au début ud tour
        self.moves_used = 0
        self.attacks_used = 0

    def current_player(self) -> Player:
        return self.turn

    def get_turn_number(self) -> int:
        return self.count

    def can_move(self) -> bool:
        """Vérifie si le joueur peut encore déplacer un dragon pour ce tour"""
        return self.moves_used < MAX_MOVES_PER_TURN

    def can_attack(self) -> bool:
        """Vérifie si le joueur peut encore attaquer pour ce tour"""
        return self.attacks_used < MAX_ATTACKS_PER_TURN

    def use_move(self):
        """Marque qu'un dragon a été déplacé ce tour"""
        self.moves_used += 1

    def use_attack(self):
        """Marque qu'une attaque a été effectuée ce tour"""
        self.attacks_used += 1