import pygame

import screen_const as sc
from component.entities.dragon import Dragonnet
from component.enum.type_entities import TypeEntitiesEnum
from events.dragonEvents import DragonEvents
from page.component.grid_component import GridComponent
from page.component.map_builder import MapBuilder
from sidepanels import draw_sidepanels


def run_game(screen, ui):
    WHITE = (240, 240, 240)
    running = True

    img_test = pygame.image.load("assets/sprites/dragonnet.png").convert_alpha()
    img_test_rect = img_test.get_rect()
    img_test_rect.topleft = (100, 100)

    # État des panneaux
    left_open = False
    right_open = False

    # Création de la grille et de la map
    grid_comp = GridComponent(
        cols=sc.COLS,
        rows=sc.ROWS,
        tile=sc.TILE_SIZE,
        origin=(sc.OFFSET_X, sc.OFFSET_Y)
    )
    builder = MapBuilder(grid_comp.grid)
    grid_comp.grid = builder.build_map()
    dragon_events = DragonEvents(grid_comp.grid, origin=(sc.OFFSET_X, sc.OFFSET_Y), tile_size=sc.TILE_SIZE)
    print(grid_comp.grid)

    dragonnet_test = Dragonnet(0, 0)
    grid_comp.grid.add_occupant(dragonnet_test, dragonnet_test.position)

    while running:

        # Dessiner le jeu
        screen.fill(WHITE)
        ui.draw(screen)
        screen.blit(img_test, img_test_rect)

        # Grille et map
        grid_comp.draw(screen)
        builder.base1.draw(screen)
        builder.base2.draw(screen)
        builder.volcano.draw(screen)
        builder.life_island.draw(screen)

        # Events
        dragon_events.draw(screen)

        # Entités de test
        dragonnet_test.draw(screen)

        # Dessiner les side panels et récupérer leurs rectangles
        left_rect, right_rect = draw_sidepanels(screen, left_open, right_open)

        for event in pygame.event.get():
            action = ui.handle_event(event)
            if action == "pause":
                return "pause"
            if event.type == pygame.MOUSEBUTTONDOWN:
                cell = grid_comp.handle_click(event.pos)
                if cell is None:
                    continue

                occ = None
                for o in cell.occupants:
                    if TypeEntitiesEnum.DRAGON in o.type_entity:
                        occ = o
                    elif occ is not None:
                        occ = o

                if occ is not None:
                    print("Cell Occupant:", occ.type_entity)
                    if TypeEntitiesEnum.DRAGON in occ.type_entity:
                        print("DRAGON sélectionné")
                        dragon_events.handle_click(event.pos, occ)
                    else:
                        dragon_events.handle_click(event.pos)
                else:
                    dragon_events.handle_click(event.pos)

        # Gérer l'ouverture/fermeture des panneaux
        mouse = pygame.mouse.get_pos()
        if left_rect.collidepoint(mouse):
            left_open = True
        else:
            left_open = False

        if right_rect.collidepoint(mouse):
            right_open = True
        else:
            right_open = False

        # Test
        dragonnet_test.update()

        pygame.display.flip()

    return None
