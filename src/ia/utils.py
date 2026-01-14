from typing import List

from src.component.entities.dragon import Dragon
from src.component.grid import Cell
from src.component.path_finding import find_path
from src.enum.type_entities import TypeEntitiesEnum


def find_distances_with_enemies(actual_entity, enemies, grid):
    results = []

    for enemy in enemies:
        path = find_path(grid, actual_entity.cell, enemy.cell)

        if path is None:
            print(
                f"No path to enemy {enemy.name} "
                f"at {enemy.cell.position.x},{enemy.cell.position.y}"
            )
            continue  # IMPORTANT

        distance = len(path)

        print(
            f"Path to enemy {enemy.name} "
            f"at {enemy.cell.position.x},{enemy.cell.position.y} "
            f"-> distance {distance}"
        )

        results.append({
            'enemy': enemy,
            'path': path,
            'distance': distance
        })

    return results


def compute_move_cells(dragon: Dragon, grid) -> List[Cell]:
    """
    Calcule toutes les cases accessibles pour le dragon
    :param dragon: instance de Dragon
    :return: liste de Position des cases accessibles
    """
    max_move = dragon.actual_speed
    start_x, start_y = dragon.cell.position.x, dragon.cell.position.y

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Droite, Gauche, Bas, Haut
    visited = set()
    possible_cells = []
    queue = [(start_x, start_y, 0)]  # liste = file FIFO
    visited.add((start_x, start_y))

    while queue:
        x, y, dist = queue.pop(0)

        if dist > 0:
            possible_cells.append(grid.cells[y][x])

        if dist == max_move:
            continue

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < grid.nb_columns and 0 <= ny < grid.nb_rows):
                continue

            if (nx, ny) in visited:
                continue

            next_cell = grid.cells[ny][nx]

            blocked = False
            for occ in next_cell.occupants:
                if TypeEntitiesEnum.OBSTACLE in occ.type_entity:
                    blocked = True
                    break

            if blocked:
                continue

            visited.add((nx, ny))
            queue.append((nx, ny, dist + 1))

    return possible_cells
