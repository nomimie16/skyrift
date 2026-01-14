from src.component.entities.dragon import Dragon
from src.component.grid import Grid
from src.ia.scoring import deplacement_score
from src.ia.scoring import deplacement_score, choose_best_action
from src.ia.utils import compute_move_cells
from src.player import Player
from src.events.dragonEvents import DragonEvents



class IAPlayer:
    def __init__(self, player: Player, ennemy: Player, grid: Grid, dragon_events: DragonEvents):
        self.player: Player = player
        self.ennemy: Player = ennemy
        self.grid: Grid = grid
        self.dragon_events = dragon_events


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

                # if dragon.moving:
                #     return

                # if dragon.has_moved:
                #     continue
                action = choose_best_action(dragon, self.grid, self.player, self.ennemy, self.dragon_events)
                print(f"IA chose action {action} for dragon {dragon.name} at ({dragon.cell.position.x},{dragon.cell.position.y})")
                if action[0] == "move":
                    dragon.move_dragon(action[1].position.x, action[1].position.y, self.grid)
                elif action[0] == "attack":
                    dragon.attack_fireball(action[1])
                dragon.has_moved = True

        #         best_cell = self.decide_move(dragon)
        #         if best_cell != dragon.cell:
        #             dragon.move_dragon(best_cell.position.x, best_cell.position.y, self.grid)
        #             dragon.has_moved = True
                best_cell = self.decide_move(self.player.units[0])
                if best_cell != dragon.cell:
                    dragon.move_dragon(best_cell.position.x, best_cell.position.y, self.grid)
                    break

        #             break





if __name__ == "__main__":
    pass
