from src.component.entities.dragon import Dragon
from src.component.grid import Cell, Grid
from src.const import DRAGON_GEANT_COST
from src.events.dragonEvents import DragonEvents
from src.player import Player


def deplacement_score(dragon: Dragon, target_cell: Cell, grid: Grid, player, enemy) -> float:
    """
    Score de la cellule target_cell pour le dragon.
    Plus le score est élevé, meilleur est le mouvement.

    Facteurs :
    - Objectif principal : se rapprocher de la base ennemie
    - Danger : proximité dragons ennemis
    - Opportunité : trésors ou dragons faibles à portée
    - Sécurité / stratégie : protéger sa base, éviter regroupement
    """

    score = 0

    if enemy.base and enemy.base.cell:
        dist_to_enemy_base = grid.distance(target_cell, enemy.base.cell)
        score += (100 - dist_to_enemy_base * 2)

    for enemy_dragon in enemy.units:
        if enemy_dragon.cell:
            dist = grid.distance(target_cell, enemy_dragon.cell)
            if dist <= enemy_dragon.attack_range and dragon.hp <= enemy_dragon.attack_damage:
                score -= 50
            elif enemy_dragon.hp <= dragon.attack_damage:
                score += 20

    if player.base and player.base.cell:
        enemy_near_base = False
        for enemy_dragon in enemy.units:
            if enemy_dragon.cell:
                dist_enemy_base = grid.distance(enemy_dragon.cell, player.base.cell)
                if dist_enemy_base <= 4:
                    enemy_near_base = True
                    break
        if enemy_near_base:
            dist_to_ally_base = grid.distance(target_cell, player.base.cell)
            score += max(0, 20 - dist_to_ally_base * 4)

    for ally_dragon in player.units:
        if ally_dragon != dragon and ally_dragon.cell:
            if target_cell == ally_dragon.cell:
                score -= 1000

    return score


def attaque_score(dragon: Dragon, target: Dragon, grid: Grid, player, enemy) -> float:
    """
    Score d'attaque pour un dragon ciblé.
    Plus le score est élevé, plus c'est intéressant d'attaquer cette cible.

    Facteurs :
    - Dégâts possibles vs HP cible
    - Sécurité : si la cible peut riposter
    - Opportunité : éliminer un dragon faible ou stratégique
    """

    score = 0

    if not target.cell:
        return score

    score += min(dragon.attack_damage, target.hp) * 10

    # cibles faibles
    if target.hp <= dragon.attack_damage:
        score += 100

    # la cible peut riposter
    dist = grid.distance(dragon.cell, target.cell)
    if dist <= target.attack_range:
        score -= 20

    if target.cell == enemy.base.cell:
        score += 40  # attaquer la base ennemie

    if target.cell == player.base.cell:
        score -= 30

    for other_enemy in enemy.units:
        if other_enemy != target and other_enemy.cell:
            dist_ennemi = grid.distance(target.cell, other_enemy.cell)
            if dist_ennemi <= 1:
                score += 10

    return score


def score_purchase_option(player, ennemy, option, current_gold):
    score = 0

    base_health_ratio = player.base.hp / player.base.max_hp
    nb_enemies = len(ennemy.units)
    nb_allies = len(player.units)

    # 1. SCORING POUR LA TOUR
    if option["name"] == "buy_tower":
        score += 50  # Base value car c'est important

        # Plus la base est blessée, plus on veut la tour (Urgence)
        score += (1.0 - base_health_ratio) * 200

        score += nb_enemies * 15

    # SCORING POUR LES DRAGONS
    elif "buy" in option["name"]:
        if option["name"] == "buy_giant":
            score += 80
        elif option["name"] == "buy_medium":
            score += 50
        elif option["name"] == "buy_small":
            score += 20

        gold_left = current_gold - option["cost"]
        if gold_left < 10:
            score -= 15

        if nb_allies == 0:
            score += 30

        # Stratégie de contre (Optionnel) : Si l'ennemi a un Géant, il me faut du lourd
        # if any(isinstance(u, DragonGeant) for u in self.ennemy.units):
        #     if option["name"] == "buy_giant": score += 20

    # 3. SCORING POUR "ATTENDRE" (WAIT)
    elif option["name"] == "wait":
        score += 10  # Base

        if current_gold < DRAGON_GEANT_COST:
            score += 20

        if base_health_ratio < 0.3:
            score -= 100

        if nb_allies == 0:
            score -= 50

    return score


def get_best_move(dragon: Dragon, grid: Grid, player: Player, enemy: Player, events):
    """
    Trouve la meilleure case su laquelle se déplacer
    :param dragon:
    :param grid:
    :param player:
    :param enemy:
    :param events:
    :return:
    """
    best_cell = None
    best_score = -float('inf')

    move_cells = events.compute_move_cells(dragon)

    if dragon.cell not in move_cells:
        move_cells.append(dragon.cell)

    for cell in move_cells:
        score = deplacement_score(dragon, cell, grid, player, enemy)
        if score > best_score:
            best_score = score
            best_cell = cell

    return best_cell, best_score


def get_best_attack(dragon: Dragon, grid: Grid, player: Player, enemy: Player):
    """
    Trouve la meilleure cible à attaquer depuis la position actuelle
    :param dragon:
    :param grid:
    :param player:
    :param enemy:
    :return:
    """
    best_target = None
    best_score = -float('inf')

    for e in enemy.units:
        if e.cell and dragon.cell and grid.distance(dragon.cell, e.cell) <= dragon.attack_range:
            score = attaque_score(dragon, e, grid, player, enemy)
            if score > best_score:
                best_score = score
                best_target = e

    return best_target, best_score


def choose_best_action(dragon: Dragon, grid: Grid, player: Player, enemy: Player, events: DragonEvents):
    """
    Retourne l'action la plus intéressante pour ce dragon
    sous forme d'un tuple : ("move", Cell) ou ("attack", Dragon)
    """
    actions = []
    print("actions possible", actions)
    # attaques possibles
    print(f"TEST CHOIX {dragon.name} ({dragon.cell.position.x},{dragon.cell.position.y})")
    for e in enemy.units:
        if e.cell and grid.distance(dragon.cell, e.cell) <= dragon.attack_range:
            actions.append(("attack", e))

    move_cells = events.compute_move_cells(dragon)
    # déplacements possibles
    for cell in move_cells:
        actions.append(("move", cell))

    # action avec le meilleur score
    best_action = ("wait", None)
    best_score = -float('inf')

    for action in actions:
        if action[0] == "attack":
            score = attaque_score(dragon, action[1], grid, player, enemy)
            score += 1000
        else:
            score = deplacement_score(dragon, action[1], grid, player, enemy)

        if score > best_score:
            best_score = score
            best_action = action

    return best_action
