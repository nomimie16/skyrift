import pygame

import screen_const as sc
from component.entities.purse import spawn_random_purse
from component.entities.tower import Tower
from component.enum.type_entities import TypeEntitiesEnum
from const import SPAWN_POS_P1, SPAWN_POS_P2
from events.dragonEvents import DragonEvents
from events.towerEvents import TowerEvents
from page.component.grid_component import GridComponent
from page.component.map_builder import MapBuilder
from page.sidepanels import draw_sidepanels
from player import Player
from turn import Turn


def run_game(screen, ui):
    WHITE = (240, 240, 240)
    running = True

    # img_test = pygame.image.load("assets/sprites/dragonnet.png").convert_alpha()
    # img_test_rect = img_test.get_rect()
    # img_test_rect.topleft = (100, 100)

    p1: Player = Player(name="Yanis", color="bleu")
    p2: Player = Player(name="Player 2", color="rouge")
    turn: Turn = Turn(p1, p2)
    player: Player = turn.current_player()

    # État des panneaux
    left_open = False
    right_open = False

    # positions initiales (panneaux fermés)
    current_left_x = -200
    current_right_x = screen.get_width()

    # Création de la grille et de la map
    grid_comp = GridComponent(
        cols=sc.COLS,
        rows=sc.ROWS,
        tile=sc.TILE_SIZE,
        origin=(sc.OFFSET_X, sc.OFFSET_Y)
    )
    builder = MapBuilder(grid_comp.grid, p1, p2)
    grid_comp.grid = builder.build_map()
    dragon_events = DragonEvents(grid_comp.grid, origin=(sc.OFFSET_X, sc.OFFSET_Y), tile_size=sc.TILE_SIZE)
    tower_events = TowerEvents(grid_comp.grid)

    dragons = []

    print(grid_comp.grid)

    # Créer le bouton tour suivant (temporaire)
    font = pygame.font.Font(None, 28)
    button_width = 150
    button_height = 50
    button_x = screen.get_width() - button_width - 5
    button_y = screen.get_height() - button_height - 40
    next_turn_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    button_color = (186, 162, 22)
    button_hover_color = (222, 192, 18)
    button_text_color = (255, 255, 255)

    while running:
        # Dessiner le jeu
        screen.fill(WHITE)
        ui.draw(screen)
        # screen.blit(img_test, img_test_rect)

        # Grille et map
        grid_comp.draw(screen)
        builder.base1.draw(screen)
        builder.tower1.draw(screen)
        builder.base2.draw(screen)
        builder.tower2.draw(screen)
        builder.volcano.draw(screen)
        builder.life_island.draw(screen)

        # Dessine les bourses pour chaque cellule en parcourant la grille
        for row in grid_comp.grid.cells:
            for cell in row:
                for occupant in cell.occupants:
                    if TypeEntitiesEnum.PLAYER_EFFECT_ZONE in occupant.type_entity:
                        occupant.draw(screen)

        # Events
        dragon_events.draw(screen)
        tower_events.draw(screen)

        for event in pygame.event.get():
            action = ui.handle_event(event)
            if action == "pause":
                return "pause"
            if event.type == pygame.MOUSEBUTTONDOWN:

                # obligée de mettre l'appel à towerevents ici sinon ça ne passe pas si on clique sur attaquer
                if tower_events.attack_button_rect and tower_events.attack_button_rect.collidepoint(event.pos):
                    tower_events.handle_click(event.pos, None, turn.current_player(), turn)
                    continue

                # Clic sur le bouton tour suivant (temporaire)
                if next_turn_button_rect.collidepoint(event.pos):
                    print("tour de ", turn.current_player().name, "terminé")
                    turn.next()

                    # Appliquer ou retirer les effets des zones sur les dragons
                    for row in grid_comp.grid.cells:
                        for cell in row:
                            cell.apply_zone_effects_end_turn()

                    spawn_random_purse(grid_comp.grid)
                    player = turn.current_player()
                    print("tour de ", turn.current_player().name, "commencé")
                    continue
                # ouverture et fermeture des panneaux
                if left_button_rect.collidepoint(event.pos):
                    left_open = not left_open
                    continue
                if right_button_rect.collidepoint(event.pos):
                    right_open = not right_open
                    continue

                # Gestion de l'apparition des bourses

                # TODO : refactoriser ca
                clicked_buy_button = False
                for button in buy_buttons:
                    if button["rect"].collidepoint(event.pos):
                        if button["can_afford"]:
                            player.economy.spend_gold(button["cost"])
                            remaining_gold = player.economy.get_gold()

                            # Achat tour de défense
                            # TODO vérification dragon dans zone de construction

                            if isinstance(button["dragon"], Tower):
                                if turn.current_player() == p1:
                                    builder.tower1.tower_activation(grid_comp.grid)
                                else:
                                    builder.tower2.tower_activation(grid_comp.grid)
                                print(grid_comp.grid)


                            else:  # Achat dragons
                                if turn.current_player() == p1:
                                    spawn_pos = SPAWN_POS_P1
                                else:
                                    spawn_pos = SPAWN_POS_P2

                                if grid_comp.grid.cells[spawn_pos[1]][spawn_pos[0]].occupants == []:

                                    # Créer une instance du dragon aux coordonnées (0, 0)
                                    dragon_class = button["dragon"].__class__
                                    new_dragon = dragon_class(spawn_pos[0], spawn_pos[1], player=turn.current_player())

                                    # Si le dragon est a p2, sa base est en bas a droite -> il doit donc être orienté vers la gauche
                                    if turn.current_player() == p2:
                                        new_dragon.update_direction("gauche")

                                    dragons.append(new_dragon)

                                    # ajoute le dragon a la grille
                                    cell = grid_comp.grid.cells[spawn_pos[1]][spawn_pos[0]]
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
                    if occ is None:
                        for o in cell.occupants:
                            if TypeEntitiesEnum.TOWER in o.type_entity:
                                occ = o
                                break

                    if dragon_events.selected_dragon is not None:
                        dragon_events.handle_click(event.pos, occ, turn.current_player(), turn)

                    else:
                        if occ and TypeEntitiesEnum.DRAGON in occ.type_entity:
                            dragon_events.handle_click(event.pos, occ, turn.current_player(), turn)

                        elif occ and TypeEntitiesEnum.TOWER in occ.type_entity:
                            tower_events.handle_click(event.pos, occ, turn.current_player(), turn)

                        else:
                            dragon_events.handle_click(event.pos, None, turn.current_player(), turn)

        # ======================================================================================

        # Supprimer les dragons morts de la grille
        for row in grid_comp.grid.cells:
            for cell in row:
                for occupant in cell.occupants:
                    if TypeEntitiesEnum.DRAGON in occupant.type_entity:
                        if occupant.is_dead():
                            print("Dragon mort détecté :", occupant.name)
                            occupant.update()
                            cell.remove_occupant(occupant)
                        else:
                            occupant.draw(screen)
                            occupant.update()

        # ======================================================================================

        # Dessiner les side panels et récupérer leurs rectangles (ils doivent être dessinés APRES les dragons)
        left_button_rect, right_button_rect, current_left_x, current_right_x, buy_buttons = draw_sidepanels(
            screen, left_open, right_open, current_left_x, current_right_x, player.economy, turn.current_player()
        )

        # Dessiner le bouton tour suivant (temporaire)
        mouse_pos = pygame.mouse.get_pos()
        button_color_to_use = button_hover_color if next_turn_button_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, button_color_to_use, next_turn_button_rect)
        pygame.draw.rect(screen, (0, 0, 0), next_turn_button_rect, 2)
        button_text = font.render("Tour suivant", True, button_text_color)
        text_rect = button_text.get_rect(center=next_turn_button_rect.center)
        screen.blit(button_text, text_rect)

        # Afficher le tour du joueur actuel (temporaire)
        turn_text = font.render(f"tour de {player.name}", True, (0, 0, 0))
        turn_text_rect = turn_text.get_rect(center=(next_turn_button_rect.centerx, next_turn_button_rect.top - 30))
        screen.blit(turn_text, turn_text_rect)

        pygame.display.flip()

    return None
