from src.component.entities.dragon import Dragon, DragonGeant, DragonMoyen, Dragonnet
from src.component.grid import Grid
from src.const import SPAWN_POS_P2, DRAGON_GEANT_COST, DRAGON_MOYEN_COST, DRAGONNET_COST, TOWER_COST
from src.enum.type_entities import TypeEntitiesEnum
from src.events.dragonEvents import DragonEvents
from src.ia.scoring import deplacement_score, score_purchase_option, get_best_attack, get_best_move
from src.ia.utils import compute_move_cells
from src.player import Player


class IAPlayer:
    def __init__(self, player: Player, ennemy: Player, grid: Grid, dragon_events: DragonEvents):
        self.player: Player = player
        self.ennemy: Player = ennemy
        self.grid: Grid = grid
        self.dragon_events = dragon_events
        self.dragon_states = {}

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

    def manage_economy(self):
        """
        Système d'achat basé sur le SCORING.
        L'IA évalue chaque option d'achat et choisit celle avec le meilleur score.
        """
        current_gold = self.player.economy.get_gold()
        spawn_x, spawn_y = SPAWN_POS_P2
        spawn_cell = self.grid.cells[spawn_y][spawn_x]

        spawn_is_free = True
        for occupant in spawn_cell.occupants:
            if TypeEntitiesEnum.PLAYER_EFFECT_ZONE in occupant.type_entity:
                continue
            if hasattr(occupant, 'moving') and occupant.moving:
                return  # On attend la fin de l'animation
            spawn_is_free = False
            break

        options = []

        if self.player.tower and self.player.tower.is_dead():
            options.append({
                "name": "buy_tower",
                "cost": TOWER_COST,
                "type": "tower"
            })

        if spawn_is_free:
            options.append({"name": "buy_giant", "cost": DRAGON_GEANT_COST, "class": DragonGeant})
            options.append({"name": "buy_medium", "cost": DRAGON_MOYEN_COST, "class": DragonMoyen})
            options.append({"name": "buy_small", "cost": DRAGONNET_COST, "class": Dragonnet})

        options.append({"name": "wait", "cost": 0})

        best_option = None
        best_score = float('-inf')

        print(f"--- Réflexion IA (Or: {current_gold}) ---")
        for option in options:
            # Si on ne peut pas payer, score impossible
            if option["cost"] > current_gold:
                continue

            score = score_purchase_option(self.player, self.ennemy, option, current_gold)
            print(f"Option {option['name']} : score {score:.1f}")

            if score > best_score:
                best_score = score
                best_option = option

        if best_option and best_option["name"] != "wait":
            print(f"IA CHOISIT : {best_option['name']}")

            if best_option["name"] == "buy_tower":
                self.player.tower.tower_activation(
                    self.grid,
                    self.player,
                    popup_manager=self.dragon_events.damage_heal_popup_manager
                )
            else:
                new_dragon = best_option["class"](spawn_x, spawn_y, self.player)
                new_dragon.update_direction("gauche")
                self.player.add_unit(new_dragon)
                self.grid.add_occupant(new_dragon, spawn_cell)

            self.player.economy.spend_gold(best_option["cost"])

    def play_turn(self, turn):

        for dragon in self.player.units:
            if isinstance(dragon, Dragon):
                if dragon.moving or dragon.has_moved:
                    continue

                # Meilleur déplcacement
                move_cell, score_move = get_best_move(dragon, self.grid, self.player, self.ennemy, self.dragon_events)
                # Meilleure attaque
                target_now, score_attack_now = get_best_attack(dragon, self.grid, self.player, self.ennemy)

                if score_attack_now > score_move:  # Attaque avant déplacement
                    dragon.attack(target_now)
                    dragon.attack_fireball(target_now)

                    if move_cell and move_cell != dragon.cell and score_move > 0:
                        self.execute_move(dragon, move_cell)

                else:  # Déplacement avant attaque

                    if move_cell and move_cell != dragon.cell:
                        self.execute_move(dragon, move_cell)

                    target_after, score_after = get_best_attack(dragon, self.grid, self.player, self.ennemy)
                    if target_after and score_after > 0:
                        dragon.attack_fireball(target_after)

                dragon.has_moved = True
        self.manage_economy()

    def execute_move(self, dragon, target_cell):
        """ Méthode utilitaire pour exécuter proprement le mouvement """
        if dragon.cell:
            self.grid.cells[dragon.cell.position.y][dragon.cell.position.x].remove_occupant(dragon)

        self.grid.add_occupant(dragon, target_cell)
        dragon.cell = target_cell
        dragon.move_dragon(target_cell.position.x, target_cell.position.y, self.grid)


if __name__ == "__main__":
    pass
