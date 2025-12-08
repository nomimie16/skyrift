from typing import List, Optional

from component.enum.type_entities import TypeEntitiesEnum
from component.grid import Grid, Cell


def heuristic(cell1: Cell, cell2: Cell) -> int:
    """Heuristique A*: distance de Manhattan
    :param cell1: première cellule
    :param cell2: deuxième cellule
    :return: distance de Manhattan entre les deux cellules
    """
    return abs(cell1.position.x - cell2.position.x) + abs(cell1.position.y - cell2.position.y)


def find_path(grid: Grid, start_cell: Cell, end_cell: Cell) -> Optional[List[Cell]]:
    """
    Trouve un chemin de start_cell à end_cell sur la grille en utilisant A*.
    Ne traverse pas les cellules contenant un OBSTACLE.
    Aide :
    - https://medium.com/@aggorjefferson/building-an-a-pathfinding-visualizer-in-python-with-pygame-a2cb3502f49e
    - https://www.geeksforgeeks.org/python/a-search-algorithm-in-python/
    - https://github.com/ademakdogan/Implementation-of-A-Algorithm-Visualization-via-Pyp5js-/blob/master/AStar.py
    :param grid: instance de Grid
    :param start_cell: cellule de départ
    :param end_cell: cellule d'arrivée
    :return: liste de cellules formant le chemin, ou None si aucun chemin n'est
    """
    open_set = [start_cell]
    came_from = {}

    g_score = {start_cell: 0}
    f_score = {start_cell: heuristic(start_cell, end_cell)}

    visited = set()

    while open_set:
        current = open_set[0]
        for cell in open_set:
            if f_score.get(cell, float('inf')) < f_score.get(current, float('inf')):
                current = cell

        if current == end_cell:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start_cell)
            return path[::-1]

        open_set.remove(current)
        visited.add(current)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = current.position.x + dx, current.position.y + dy
            if 0 <= nx < grid.nb_columns and 0 <= ny < grid.nb_rows:
                neighbor = grid.cells[ny][nx]

                if neighbor != end_cell:
                    blocked = False
                    for occ in neighbor.occupants:
                        if TypeEntitiesEnum.OBSTACLE in occ.type_entity:
                            blocked = True
                            break
                    if blocked:
                        continue

                tentative_g_score = g_score[current] + 1

                if neighbor in visited and tentative_g_score >= g_score.get(neighbor, float('inf')):
                    continue

                if neighbor not in open_set:
                    open_set.append(neighbor)

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end_cell)

    return None
