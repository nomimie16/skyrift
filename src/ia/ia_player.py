from src.component.entities.dragon import Dragon
from src.component.grid import Grid
from src.ia.scoring import deplacement_score
from src.ia.utils import compute_move_cells
from src.player import Player


class IAPlayer:
    def __init__(self, player: Player, ennemy: Player, grid: Grid):
        self.player: Player = player
        self.ennemy: Player = ennemy
        self.grid: Grid = grid

    def decide_move(self, dragon):
        best_score = float('-inf')
        best_cell = dragon.cell

        accessible_cells = compute_move_cells(dragon, self.grid)

        for cell in accessible_cells:
            score = deplacement_score(dragon, cell, self.grid, self.player, self.ennemy)
            if score > best_score:
                best_score = score
                best_cell = cell

        return best_cell

    def play_turn(self, turn):

        for dragon in self.player.units:
            if isinstance(dragon, Dragon):
                best_cell = self.decide_move(self.player.units[0])
                if best_cell != dragon.cell:
                    dragon.move_dragon(best_cell.position.x, best_cell.position.y, self.grid)
                    break


if __name__ == "__main__":
    pass
