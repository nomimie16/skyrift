from src.component.entities.dragon import Dragon, DragonGeant, DragonMoyen, Dragonnet
from src.component.grid import Grid
from src.const import SPAWN_POS_P2, DRAGON_GEANT_COST, DRAGON_MOYEN_COST, DRAGONNET_COST, TOWER_COST, SPAWN_POS_P1
from src.enum.type_entities import TypeEntitiesEnum
from src.events.dragonEvents import DragonEvents
from src.ia.scoring import score_purchase_option, get_best_attack, get_best_move
from src.player import Player


class IAPlayer:
    def __init__(self, player: Player, ennemy: Player, grid: Grid, dragon_events: DragonEvents):
        self.player: Player = player
        self.ennemy: Player = ennemy
        self.grid: Grid = grid
        self.dragon_events = dragon_events

    def random_start(self):
        pass

    def manage_economy(self):
        """
        Système d'achat basé sur le SCORING.
        L'IA évalue chaque option d'achat et choisit celle avec le meilleur score.
        """
        current_gold = self.player.economy.get_gold()
        spawn_x, spawn_y = (0, 0)
        if self.player.color == "bleu":
            spawn_x, spawn_y = SPAWN_POS_P1
        elif self.player.color == "rouge":
            spawn_x, spawn_y = SPAWN_POS_P2
        spawn_cell = self.grid.cells[spawn_y][spawn_x]

        danger_score = 0.0

        if self.player.base:
            # on regarde la vie de la base, si <50% alors le danger augmente
            base_hp_ratio = self.player.base.hp / self.player.base.max_hp
            if base_hp_ratio < 0.5:
                danger_score += (0.5 - base_hp_ratio) * 2

        min_dist = float('inf')
        if self.player.base and self.player.base.cell:
            for unit in self.ennemy.units:
                if unit.cell:
                    distance = self.grid.distance(unit.cell, self.player.base.cell)
                    if distance < min_dist:
                        min_dist = distance
            # si dragons ennemies prés de la base alors la danger augmente
            if min_dist < 8:
                danger_score += (8 - min_dist) / 8.0

        danger_score = min(danger_score, 1.0)

        spawn_is_free = True
        for occupant in spawn_cell.occupants:
            if TypeEntitiesEnum.PLAYER_EFFECT_ZONE in occupant.type_entity:
                continue
            if hasattr(occupant, 'moving') and occupant.moving:
                return  # On attend la fin de l'animation
            spawn_is_free = False
            break

        options = []

        if self.player.tower and not self.player.tower.active:
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

        for option in options:
            # Si on ne peut pas payer, score impossible
            if option["cost"] > current_gold:
                continue

            score = score_purchase_option(self.player, self.ennemy, option, current_gold, danger_score)
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
                direction = "droite" if self.player.color == "bleu" else "gauche"
                new_dragon.update_direction(direction)
                self.player.add_unit(new_dragon)
                self.grid.add_occupant(new_dragon, spawn_cell)

            self.player.economy.spend_gold(best_option["cost"])

    def play_turn(self, turn):

        for dragon in self.player.units:
            if not isinstance(dragon, Dragon):
                continue
            if dragon.moving or dragon.has_moved:
                continue


            target_now, score_attack_now = get_best_attack(dragon, self.grid, self.player, self.ennemy)

            move_cell, score_move = get_best_move(dragon, self.grid, self.player, self.ennemy, self.dragon_events, turn)

            target_after_move = None
            score_attack_after = 0
            if move_cell and move_cell != dragon.cell:
                # change la position temporairement pour tester
                old_cell = dragon.cell
                dragon.cell = move_cell
                target_after_move, score_attack_after = get_best_attack(dragon, self.grid, self.player, self.ennemy)
                dragon.cell = old_cell

            # on priosise le mouvement avant l'attaque, sauf si attaquer tout de suite st clairement mieux
            should_attack_first = (
                target_now and score_attack_now > 0 and
                (score_attack_now >= score_attack_after or not move_cell or move_cell == dragon.cell)
            )

            if should_attack_first:
                if not dragon.has_attacked:
                    dragon.attack(target_now)
                    dragon.attack_fireball(target_now)

                if move_cell and move_cell != dragon.cell:
                    self.execute_move(dragon, move_cell)
            else:
                if move_cell and move_cell != dragon.cell:
                    self.execute_move(dragon, move_cell)

                target_after, score_after = get_best_attack(dragon, self.grid, self.player, self.ennemy)
                if target_after and score_after > 0 and not dragon.has_attacked:
                    dragon.attack(target_after)
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
