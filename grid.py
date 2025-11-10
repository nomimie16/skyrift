from component.entities.dragon import Dragonnet
from component.position import Position

import pygame
from win32api import GetSystemMetrics 



class Cell:
    """Definition of a grid cell"""
    def __init__(self, x, y):
        self._position = Position(x, y)
        self._occupant = None

    def get_occupant(self):
        """return the current occupant"""
        return self._occupant
    
    def get_position(self, occupant):
        if occupant.position:
            return occupant.position
        return None

    def __str__(self):
        """Display the cell"""
        if self._occupant:
            return "occupe"
        return str(self._position)

    def __repr__(self):
        return str(self)


class Grid:
    
    """Definition of a game board grid"""
    def __init__(self, nb_columns, nb_rows):
        self.nb_columns = nb_columns
        self.nb_rows = nb_rows
        self.cells = [[Cell(x, y) for x in range(nb_columns)] for y in range(nb_rows)]

    def add_occupant(self, occupant, position: Position):
        """Place an occupant (e.g., a dragon) on the grid"""
        x = position.get_x()
        y = position.get_y()
        if not (0 <= x < self.nb_columns) or not (0 <= y < self.nb_rows):
            print(f"Position ({x}, {y}) is out of grid")
            return False
        cell = self.cells[y][x]
        if cell._occupant is None:
            cell._occupant = occupant
            occupant.position = cell._position
            return True
        return False
    
    def distance(self,occupant1, occupant2):
        x1, y1 = occupant1.position.x, occupant1.position.y
        x2, y2 = occupant2.position.x, occupant2.position.y
        
        return abs(x1 - x2) + abs(y1 - y2)

    def __str__(self):
        """Display the entire grid"""
        return "\n".join(
            " | ".join(str(cell) for cell in row)
            for row in self.cells
        )


# if __name__ == '__main__':
#     # Initialiser Pygame
#     pygame.init()
    
#     # Créer la fenêtre
#     taille_ecran = GetSystemMetrics(1)
#     screen = pygame.display.set_mode((taille_ecran, taille_ecran))
    
#     # Définir les couleurs
#     WHITE = (255, 255, 255)
    
#     # Bouton quitter le jeu
#     quit_img = pygame.image.load("assets/img/quit.png").convert_alpha()
#     quit_img = pygame.transform.scale(quit_img, (55, 55))
#     quit_rect = quit_img.get_rect()
#     quit_rect.topleft = (taille_ecran - 50, 0)

#     # Police pour le texte
#     # font = pygame.font.Font(None, 36)
    
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
    
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if quit_rect.collidepoint(event.pos):
#                     running = False
#                     print("##################\nJeu SkyRift Fermé.\n##################")
                    
    
#         # Remplir l'écran avec du blanc
#         screen.fill(WHITE)
        
#         # Dessiner le bouton quitter
#         screen.blit(quit_img, quit_rect)
    
        


#     pos1 = Position(0, 0)
#     pos2 = Position(1, 4)

#     Dragon1 = Dragonnet(0,0)
#     Dragon2 = Dragonnet(1,4)

#     # Create the grid
#     grid = Grid(5, 5)

#     # Test add methode
#     grid.add_occupant(Dragon1, pos1)
#     grid.add_occupant(Dragon2, pos2)
#     distance = grid.distance(Dragon1, Dragon2)

#     print(f"Grid 1:\n{grid}")
#     print(f"Distance :\n{distance}")

#     # Mettre à jour l'affichage
#     # pygame.display.flip()
#     # # # Test move method (if needed)
#     # # pos2.move(3, 2)
#     # # print(f"Position 2 (+3x, +2y): {pos2}")
#     # # pos3.move(-12, 2)
#     # # print(f"Position 3 (-12x, +2y): {pos3}")

#     # pygame.quit()

