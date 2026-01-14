from src.component.entities.dragon import Dragon
from src.component.grid import Cell, Grid
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
        score += max(0, 100 - dist_to_enemy_base * 5)

    for enemy_dragon in enemy.units:
        if enemy_dragon.cell:
            dist = grid.distance(target_cell, enemy_dragon.cell)
            if dist <= enemy_dragon.attack_range and dragon.hp <= enemy_dragon.attack_damage:
                score -= 50
            elif enemy_dragon.hp <= dragon.attack_damage:
                score += (dragon.attack_damage / max(enemy_dragon.hp, 1)) * 30

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
            dist_to_ally = grid.distance(target_cell, ally_dragon.cell)
            if dist_to_ally == 0:
                score -= 10

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


def choose_best_action(dragon: Dragon, grid: Grid, player: Player, enemy: Player, events: DragonEvents):
    """
    Retourne l'action la plus intéressante pour ce dragon
    sous forme d'un tuple : ("move", Cell) ou ("attack", Dragon)
    """
    actions = []
    print("actions possible",actions)
    # attaques possibles
    print(f"TEST CHOIX {dragon.name} ({dragon.cell.position.x},{dragon.cell.position.y})")
    for e in enemy.units:
        if e.cell and grid.distance(dragon.cell, e.cell) <= dragon.attack_range:
            actions.append(("attack", e))

    # déplacements possibles
    for cell in events.compute_move_cells(dragon):
        actions.append(("move", cell))

    # action avec le meilleur score
    best_action = ("pass", None)
    best_score = -float('inf')

    for action in actions:
        if action[0] == "attack":
            score = attaque_score(dragon, action[1], grid, player, enemy)
        else:
            score = deplacement_score(dragon, action[1], grid, player, enemy)

        if score > best_score:
            best_score = score
            best_action = action

    return best_action