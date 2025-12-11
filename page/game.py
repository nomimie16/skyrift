import pygame

import screen_const as sc
from component.entities.dragon import Dragonnet, DragonGeant
from component.enum.type_entities import TypeEntitiesEnum
from events.dragonEvents import DragonEvents
from page.component.grid_component import GridComponent
from page.component.map_builder import MapBuilder
from page.sidepanels import draw_sidepanels
from economy import Economy

SPAWN_POS = (0, 0) # TODO : mettre ca au bon endroit


def run_game(screen, ui):
    WHITE = (240, 240, 240)
    running = True

    # img_test = pygame.image.load("assets/sprites/dragonnet.png").convert_alpha()
    # img_test_rect = img_test.get_rect()
    # img_test_rect.topleft = (100, 100)

    # État des panneaux
    left_open = False
    right_open = False

    # positions initiales (panneaux fermés)
    current_left_x = -200
    current_right_x = screen.get_width()  

    economy = Economy()

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

    dragons = []
    x, y = 0, 0
    dragonnet_test = Dragonnet(x, y)
    cell = grid_comp.grid.cells[y][x]
    grid_comp.grid.add_occupant(dragonnet_test, cell)
    x, y = 0, 1
    dragon_geant_test = DragonGeant(x, y)
    cell = grid_comp.grid.cells[y][x]
    grid_comp.grid.add_occupant(dragon_geant_test, cell)
    dragons.append(dragon_geant_test)
    dragons.append(dragonnet_test)
    dragonnet_test.hp = 4

    print(grid_comp.grid)

    while running:

        # Dessiner le jeu
        screen.fill(WHITE)
        ui.draw(screen)
        # screen.blit(img_test, img_test_rect)

        # Grille et map
        grid_comp.draw(screen)
        builder.base1.draw(screen)
        builder.base2.draw(screen)
        builder.volcano.draw(screen)
        builder.life_island.draw(screen)

        # Events
        dragon_events.draw(screen)

        for event in pygame.event.get():
            action = ui.handle_event(event)
            if action == "pause":
                return "pause"
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ouverture et fermeture des panneaux
                if left_button_rect.collidepoint(event.pos):
                    left_open = not left_open
                    continue
                if right_button_rect.collidepoint(event.pos):
                    right_open = not right_open
                    continue

                # TODO : refactoriser ca
                clicked_buy_button = False
                for button in buy_buttons:
                    if button["rect"].collidepoint(event.pos):
                        if button["can_afford"]:
                            if grid_comp.grid.cells[SPAWN_POS[0]][SPAWN_POS[1]].occupants == []:
                                economy.spend_gold(button["cost"])
                                remaining_gold = economy.get_gold()

                                # Créer une instance du dragon aux coordonnées (0, 0)
                                dragon_class = button["dragon"].__class__
                                new_dragon = dragon_class(SPAWN_POS[0], SPAWN_POS[1])
                                dragons.append(new_dragon)

                                # ajoute le dragon a la grille
                                cell = grid_comp.grid.cells[SPAWN_POS[0]][SPAWN_POS[1]]
                                grid_comp.grid.add_occupant(new_dragon, cell)


                                # logs
                                print(f"{button['name']} acheté ! argent restant : {remaining_gold}")
                                print(f"inventaire de dragons : {[d.name for d in dragons]}")
                            else:
                                print("Impossible d'acheter : la case de spawn est occupée.")
                        else:
                            print("Impossible d'acheter : fonds insuffisants.")
                        clicked_buy_button = True

                if not clicked_buy_button:
                    cell = grid_comp.handle_click(event.pos)
                    if cell is None:
                        continue

                    occ = None
                    for o in cell.occupants:
                        if TypeEntitiesEnum.DRAGON in o.type_entity:
                            occ = o
                            break
                        elif occ is not None:
                            occ = o

                    if occ is not None:
                        if TypeEntitiesEnum.DRAGON in occ.type_entity:
                            dragon_events.handle_click(event.pos, occ)
                        else:
                            dragon_events.handle_click(event.pos)
                    else:
                        dragon_events.handle_click(event.pos)

        # ======================================================================================
        # Appliquer les effets des zones sur les dragons
        for row in grid_comp.grid.cells:
            for cell in row:
                cell.apply_effects()

        # Supprimer les dragons morts de la grille
        for row in grid_comp.grid.cells:
            for cell in row:
                for occupant in cell.occupants:
                    if TypeEntitiesEnum.DRAGON in occupant.type_entity:
                        if occupant.is_dead():
                            print("Dragon mort détecté :", occupant.name)
                            occupant.update(grid_comp.grid)
                            cell.remove_occupant(occupant)
                        else:
                            occupant.draw(screen)
                            occupant.update(grid_comp.grid)

        #
        # for dragon in dragons:
        #     if not dragon.is_dead():
        #         dragon.update(grid_comp.grid)
        #         dragon.draw(screen)

        # ======================================================================================
        
        # Dessiner les side panels et récupérer leurs rectangles (ils doivent être dessinés APRES les dragons)
        left_button_rect, right_button_rect, current_left_x, current_right_x, buy_buttons = draw_sidepanels(
            screen, left_open, right_open, current_left_x, current_right_x, economy
        )

        pygame.display.flip()

    return None
