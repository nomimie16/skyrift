from src.component.entities.dragon import Dragon
from src.component.grid import Cell, Grid


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
