from src.component.entities.dragon import Dragon
from src.component.grid import Cell, Grid
from src.const import DRAGON_GEANT_COST
from src.enum.type_entities import TypeEntitiesEnum
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

    if target_cell == dragon.cell:
        score -= 5

    if enemy.base and enemy.base.cell:  # objectif principal
        dist_base_enemy = grid.distance(target_cell, enemy.base.cell)
        score += (100 - dist_base_enemy) * 5

    dist_base_ally = 0
    if player.base and player.base.cell:
        dist_base_ally = grid.distance(target_cell, player.base.cell)

    dist_base_enemy = float('inf')
    if enemy.base and enemy.base.cell:
        dist_base_enemy = grid.distance(target_cell, enemy.base.cell)

    for occupant in target_cell.occupants:

        # L'ia va vouloir éviter les mauvais effets de zones-
        if TypeEntitiesEnum.VOLCANO in occupant.type_entity or TypeEntitiesEnum.TORNADO in occupant.type_entity or TypeEntitiesEnum.BAD_EFFECT_ZONE in occupant.type_entity:
            score -= 500

        if TypeEntitiesEnum.PLAYER_EFFECT_ZONE in occupant.type_entity:
            score += 40
            if player.economy.get_gold() < 300:  # bonus si peu d'argent
                score += 30

        if TypeEntitiesEnum.ISLAND_OF_LIFE in occupant.type_entity:
            if dragon.hp < dragon.max_hp:
                # Plus on est blessé, plus on veut y aller
                missing_hp_ratio = 1 - (dragon.hp / dragon.max_hp)
                score += 200 * missing_hp_ratio

    closest_enemy_dist = float('inf')

    for enemy in enemy.units:
        if not enemy.cell:
            continue

        dist = grid.distance(target_cell, enemy.cell)
        closest_enemy_dist = min(closest_enemy_dist, dist)

        if dist <= dragon.attack_range:
            enemy_range = getattr(enemy, 'attack_range', 0)
            if dist > enemy_range:
                score += 150
            else:
                score += 50
                if dragon.hp > enemy.hp:
                    score += 30

        elif dist <= getattr(enemy, 'attack_range', 0):
            score -= 100  # Zone de danger

    if closest_enemy_dist < 15:  # Si un ennemi est dans un rayon de 15 cases
        # On veut réduire la distance avec l'ennemi le plus proche
        if closest_enemy_dist > dragon.attack_range:
            score += (15 - closest_enemy_dist) * 5
    else:
        # Sinon, mouvement standard vers la base ennemie
        score += (100 - dist_base_enemy) * 2.5

    if dist_base_ally < 2:  # ne pas rester coller au spawn
        score -= 50

    # for ally in player.units:
    #     if ally != dragon and ally.cell:
    #         dist_ally = grid.distance(target_cell, ally.cell)
    #
    #         if dist_ally == 0:
    #             score -= 1000
    #         elif dist_ally == 1:
    #             if closest_enemy_dist > dragon.attack_range:
    #                 score -= 2

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

    # Possibilité d'attaquer donc augmentation score
    score += min(dragon.attack_damage, target.hp) * 10

    # cibles faibles, attaque seul
    if target.hp <= dragon.attack_damage:
        score += 500  # mort détecté donc augmentation importante du score


    else:
        # attaque à plusieurs possible
        potential_damage_allies = 0
        for ally in player.units:
            if ally != dragon and ally.cell and not ally.has_attacked:
                dist = grid.distance(ally.cell, target.cell)
                if dist <= ally.attack_range:
                    potential_damage_allies += ally.attack_damage

        if target.hp <= (dragon.attack_damage + potential_damage_allies):
            score += 200  # bonus important pour inciter
            # Plus la cible est grosse (Géant, Tour), plus on veut faire un kill collectif
            score += target.max_hp * 0.5

    # la cible peut riposter
    if target.hp > dragon.attack_damage:
        dist = grid.distance(dragon.cell, target.cell)
        if hasattr(target, 'attack_range'):
            target_range = target.attack_range
        else:
            target_range = 0

        if dist <= target_range:
            if hasattr(target, 'attack_damage'):
                target_dmg = target.attack_damage
            else:
                target_dmg = 0
            if dragon.hp <= target_dmg:
                # si reposte tue alors on retire du score
                score -= 100
            else:
                # Si juste un échange de coup alors on baisse moins
                score -= 30

    if target.hp < target.max_hp:
        # Plus le % de vie est bas, plus le score monte
        percent_missing = 1.0 - (target.hp / target.max_hp)
        score += percent_missing * 50

    if target.cell == enemy.base.cell:
        score += 150  # attaquer la base ennemie

    if target.cell == enemy.tower.cell:
        score += 200  # attaquer la tour  ennemie

    return score


def score_purchase_option(player, ennemy, option, current_gold, danger_score):
    """
    Score d'achat prenant en compte l'économie et le danger.
    :param player: Joueur actuel (IA)
    :param ennemy: Joueur Ennemie
    :param option: Options d'achats possibles
    :param current_gold: Monnaie actuelle
    :param danger_score: Score de danger
    :return:
    """
    score = 0
    nb_allies = len(player.units)

    # Score pour la tour
    if option["name"] == "buy_tower":
        score += 100

        score += danger_score * 800  # plus la base est en danger, plus la tour est utile

        score += len(ennemy.units) * 20  # si beaucoup d'ennemie c'est intérressant aussi

    # SCORING POUR LES DRAGONS
    elif "buy" in option["name"]:
        if option["name"] == "buy_giant":
            score += 100
        elif option["name"] == "buy_medium":
            score += 60
        elif option["name"] == "buy_small":
            score += 20

        if danger_score > 0.6:
            # On sort n'importe quelle unités pour défendre
            if option["name"] == "buy_small":
                score += 80
            elif option["name"] == "buy_medium":
                score += 50
        else:
            # on pénalise petite unités pour économiser pour des plus importantes
            if option["name"] == "buy_small":
                score -= 50
            elif option["name"] == "buy_medium":
                score += 10

        if nb_allies == 0:  # si aucune unité on en achère une
            score += 200

        elif option["name"] == "wait":  # attendre au lieu d'acheter
            score += 10

            if danger_score > 0.7:  # si danger critique alors pas d'attente
                score -= 500

            if current_gold > 1000:  # si beaucoup de gold  alors on achète
                score -= 100

            if danger_score < 0.3 and current_gold < DRAGON_GEANT_COST:  # si danger faible on économise
                score += 150

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

    potential_targets = list(enemy.units)

    if enemy.base and not enemy.base.is_dead():
        potential_targets.append(enemy.base)

    if enemy.tower.active:
        potential_targets.append(enemy.tower)

    for e in potential_targets:
        if e.cell and dragon.cell and grid.distance(dragon.cell, e.cell) <= dragon.attack_range:
            score = attaque_score(dragon, e, grid, player, enemy)

            if e == enemy.base:
                score += 10
            if e == enemy.tower:
                score += 5

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
