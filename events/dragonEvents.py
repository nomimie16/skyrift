# dragonevents.py
from component.position import Position


class DragonEvents:
    """
    Gestion des interactions avec les dragons :
    - sélection d'un dragon
    - déplacement vers une case vide dans la portée (speed)
    """

    def __init__(self, grid, offset_x=0, offset_y=0, tile_size=64):
        self.grid = grid
        self.selected_dragon = None
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.tile_size = tile_size

    def set_offsets(self, offset_x, offset_y):
        """Met à jour les offsets pour la conversion pixels -> case"""
        self.offset_x = offset_x
        self.offset_y = offset_y

    def handle_click(self, mouse_pos):
        """
        Gestion du clic souris
        :param mouse_pos: tuple (x, y) en pixels
        """
        print("Gestion du clic souris à la position :", mouse_pos)
        mouse_x, mouse_y = mouse_pos

        # Conversion pixels -> case
        col = (mouse_x - self.offset_x) // self.tile_size
        row = (mouse_y - self.offset_y) // self.tile_size
        print(f"Clic sur la case : ({col}, {row})")

        # Vérifier qu'on est bien dans la grille
        if not (0 <= col < self.grid.nb_columns and 0 <= row < self.grid.nb_rows):
            return

        cell = self.grid.cells[row][col]

        if cell.occupant:
            # Si clic sur un dragon, on le sélectionne
            self.selected_dragon = cell.occupant
        elif self.selected_dragon:
            # Sinon, tenter de déplacer le dragon vers une case vide
            target_pos = Position(col, row)
            # Distance Manhattan
            distance = abs(self.selected_dragon.grid_pos.x - target_pos.x) + \
                       abs(self.selected_dragon.grid_pos.y - target_pos.y)

            if distance <= self.selected_dragon._actual_speed and cell.occupant is None:
                # Déplacer le dragon
                self.selected_dragon.move_dragon(target_pos.x, target_pos.y)

                # Mettre à jour la grille
                old_x = self.selected_dragon.grid_pos.x
                old_y = self.selected_dragon.grid_pos.y
                self.grid.cells[old_y][old_x].occupant = None
                self.grid.add_occupant(self.selected_dragon, target_pos)

                # Désélectionner le dragon après mouvement
                self.selected_dragon = None
            else:
                print("Déplacement impossible : trop loin ou case occupée")
