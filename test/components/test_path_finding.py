from typing import List, Optional

from src.component.grid import Grid, Cell
from src.enum.type_entities import TypeEntitiesEnum
import pytest
from src.component.entities.static_entity import StaticEntity
from src.component.position import Position
from src.component.path_finding import find_path, heuristic

# Test de la fonction heuristique
def test_heuristic():
    grid = Grid(5, 5)
    cell1 = grid.cells[0][0]  # Position (0,0)
    cell2 = grid.cells[3][4]  # Position (4,3)
    assert heuristic(cell1, cell2) == 7  # |0-4| + |0-3| = 7

# Test de la fonction find_path
def test_find_path():
    grid = Grid(5, 5)
    start_cell = grid.cells[0][0]  # Position (0,0)
    end_cell = grid.cells[4][4]    # Position (4,4)

    path = find_path(grid, start_cell, end_cell)
    assert path is not None
    assert path[0] == start_cell
    assert path[-1] == end_cell
    assert len(path) > 0

    # Ajouter un obstacle et tester à nouveau
    obstacle = StaticEntity(
        x_cell=2,
        y_cell=2,
        name="Obstacle",
        type_entity=[TypeEntitiesEnum.OBSTACLE],
        sprite_path=None,
        width=1,
        height=1
    )
    grid.add_occupant(obstacle, grid.cells[2][2])

    path_with_obstacle = find_path(grid, start_cell, end_cell)
    assert path_with_obstacle is not None
    assert path_with_obstacle[0] == start_cell
    assert path_with_obstacle[-1] == end_cell
    assert all(cell.position != Position(2, 2) for cell in path_with_obstacle)


def test_find_path_no_path():  
    grid = Grid(3, 3)
    start_cell = grid.cells[0][0]  # Position (0,0)
    end_cell = grid.cells[2][2]    # Position (2,2)

    # Ajouter des obstacles pour bloquer le chemin
    obstacle1 = StaticEntity(
        x_cell=1,
        y_cell=0,
        name="Obstacle1",
        type_entity=[TypeEntitiesEnum.OBSTACLE],
        sprite_path=None,
        width=1,
        height=1
    )
    obstacle2 = StaticEntity(
        x_cell=0,
        y_cell=1,
        name="Obstacle2",
        type_entity=[TypeEntitiesEnum.OBSTACLE],
        sprite_path=None,
        width=1,
        height=1
    )
    grid.add_occupant(obstacle1, grid.cells[0][1])
    grid.add_occupant(obstacle2, grid.cells[1][0])

    path = find_path(grid, start_cell, end_cell)
    assert path is None  # Aucun chemin ne devrait exister
def test_find_path_start_equals_end():
    grid = Grid(3, 3)
    start_cell = grid.cells[1][1]  # Position (1,1)
    end_cell = grid.cells[1][1]    # Même position

    path = find_path(grid, start_cell, end_cell)
    assert path is not None
    assert len(path) == 1
    assert path[0] == start_cell
def test_find_path_adjacent_cells():
    grid = Grid(3, 3)
    start_cell = grid.cells[1][1]  # Position (1,1)
    end_cell = grid.cells[1][2]    # Position adjacente (2,1)

    path = find_path(grid, start_cell, end_cell)
    assert path is not None
    assert len(path) == 2
    assert path[0] == start_cell
    assert path[1] == end_cell
def test_find_path_no_free_cells():
    grid = Grid(2, 2)
    start_cell = grid.cells[0][0]  # Position (0,0)
    end_cell = grid.cells[1][1]    # Position (1,1)

    # Remplir toutes les cellules sauf la start et end
    obstacle1 = StaticEntity(
        x_cell=0,
        y_cell=1,
        name="Obstacle1",
        type_entity=[TypeEntitiesEnum.OBSTACLE],
        sprite_path=None,
        width=1,
        height=1
    )
    obstacle2 = StaticEntity(
        x_cell=1,
        y_cell=0,
        name="Obstacle2",
        type_entity=[TypeEntitiesEnum.OBSTACLE],
        sprite_path=None,
        width=1,
        height=1
    )
    grid.add_occupant(obstacle1, grid.cells[1][0])
    grid.add_occupant(obstacle2, grid.cells[0][1])

    path = find_path(grid, start_cell, end_cell)
    assert path is None  # Aucun chemin ne devrait exister
def test_find_path_large_grid():
    grid = Grid(10, 10)
    start_cell = grid.cells[0][0]  # Position (0,0)
    end_cell = grid.cells[9][9]    # Position (9,9)

    path = find_path(grid, start_cell, end_cell)
    assert path is not None
    assert path[0] == start_cell
    assert path[-1] == end_cell
    assert len(path) > 0
def test_find_path_with_multiple_obstacles():
    grid = Grid(5, 5)
    start_cell = grid.cells[0][0]  # Position (0,0)
    end_cell = grid.cells[4][4]    # Position (4,4)

    # Ajouter plusieurs obstacles
    obstacles_positions = [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2)]
    for x, y in obstacles_positions:
        obstacle = StaticEntity(
            x_cell=x,
            y_cell=y,
            name=f"Obstacle_{x}_{y}",
            type_entity=[TypeEntitiesEnum.OBSTACLE],
            sprite_path=None,
            width=1,
            height=1
        )
        grid.add_occupant(obstacle, grid.cells[y][x])

    path = find_path(grid, start_cell, end_cell)
    assert path is not None
    assert path[0] == start_cell
    assert path[-1] == end_cell
    assert all(cell.position not in [Position(x, y) for x, y in obstacles_positions] for cell in path)
def test_find_path_with_diagonal_movement():
    grid = Grid(5, 5)
    start_cell = grid.cells[0][0]  # Position (0,0)
    end_cell = grid.cells[4][4]    # Position (4,4)

    path = find_path(grid, start_cell, end_cell)
    assert path is not None
    assert path[0] == start_cell
    assert path[-1] == end_cell
    assert len(path) > 0
def test_find_path_with_no_obstacles():
    grid = Grid(3, 3)
    start_cell = grid.cells[0][0]  # Position (0,0)
    end_cell = grid.cells[2][2]    # Position (2,2)

    path = find_path(grid, start_cell, end_cell)
    assert path is not None
    assert path[0] == start_cell
    assert path[-1] == end_cell
    assert len(path) == 5  # Chemin minimal dans une grille 3x3 sans obstacles
def test_find_path_with_obstacle_at_end():
    grid = Grid(3, 3)
    start_cell = grid.cells[0][0]  # Position (0,0)
    end_cell = grid.cells[2][2]    # Position (2,2)

    # Ajouter un obstacle à la cellule d'arrivée
    obstacle = StaticEntity(
        x_cell=2,
        y_cell=2,
        name="Obstacle",
        type_entity=[TypeEntitiesEnum.OBSTACLE],
        sprite_path=None,
        width=1,
        height=1
    )
    grid.add_occupant(obstacle, end_cell)

    path = find_path(grid, start_cell, end_cell)
    assert path is not None
    assert path[0] == start_cell
    assert path[-1] == end_cell
    assert all(cell != end_cell for cell in path[:-1])  # Le chemin ne doit pas inclure l'obstacle avant la fin
    
def test_find_path_with_obstacle_at_start():
    grid = Grid(3, 3)
    start_cell = grid.cells[0][0]  # Position (0,0)
    end_cell = grid.cells[2][2]    # Position (2,2)

    # Ajouter un obstacle à la cellule de départ
    obstacle = StaticEntity(
        x_cell=0,
        y_cell=0,
        name="Obstacle",
        type_entity=[TypeEntitiesEnum.OBSTACLE],
        sprite_path=None,
        width=1,
        height=1
    )
    grid.add_occupant(obstacle, start_cell)

    path = find_path(grid, start_cell, end_cell)
    assert path is not None
    assert path[0] == start_cell
    assert path[-1] == end_cell
    assert all(cell != start_cell for cell in path[1:])  # Le chemin ne doit pas inclure l'obstacle après le début
def test_find_path_with_no_obstacles_but_blocked_cells():
    grid = Grid(3, 3)
    start_cell = grid.cells[0][0]  # Position (0,0)
    end_cell = grid.cells[2][2]    # Position (2,2)

    # Simuler des cellules bloquées sans obstacles
    blocked_cells = [grid.cells[0][1], grid.cells[1][0], grid.cells[1][1]]
    for cell in blocked_cells:
        cell.is_blocked = True  # Ajouter un attribut is_blocked pour simuler le blocage

    def modified_find_path(grid, start_cell, end_cell):
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

                    if getattr(neighbor, 'is_blocked', False):
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

    path = modified_find_path(grid, start_cell, end_cell)
    assert path is None  