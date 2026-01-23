import pygame

from src import screen_const as sc
from src.component.entities.purse import spawn_random_purse
from src.component.entities.tower import Tower
from src.const import *
from src.enum.event_enum import TypeEventEnum
from src.enum.type_entities import TypeEntitiesEnum
from src.events.dragonEvents import DragonEvents
from src.events.towerEvents import TowerEvents
from src.page.component.banner_information import BannerInformation
from src.page.component.damage_heal_popup import DamageAndHealPopupManager
from src.page.component.gold_popup import GoldPopupManager
from src.page.component.grid_component import GridComponent
from src.page.component.map_builder import MapBuilder
from src.page.component.turn_popup import TurnPopup
from src.page.sidepanels import draw_sidepanels
from src.player import Player
from src.turn import Turn


class Game:

    def __init__(self, screen, ui):
        self.screen = screen
        self.ui = ui

        # Joueurs
        self.p1 = Player(name="Yanis", color="bleu")
        self.p2 = Player(name="Player 2", color="rouge")

        self.turn = Turn(self.p1, self.p2)
        player = self.turn.current_player()

        # POPUP
        self.turn_popup = TurnPopup(duration=2000)
        self.turn_popup.show(player.name)

        self.damage_heal_popup_manager = DamageAndHealPopupManager()
        self.gold_popup_manager = GoldPopupManager()

        # Listener pour l'or
        self.p1.economy.add_listener(self.on_gold_change)
        self.p2.economy.add_listener(self.on_gold_change)

        # État des panneaux
        self.left_open = False
        self.right_open = False
        self.current_left_x = -200
        self.current_right_x = screen.get_width()

        # Création de la grille et de la map
        self.grid_comp = GridComponent(
            cols=sc.COLS,
            rows=sc.ROWS,
            tile=sc.TILE_SIZE,
            origin=(sc.OFFSET_X, sc.OFFSET_Y)
        )
        self.builder = MapBuilder(self.grid_comp.grid, self.p1, self.p2)
        self.grid_comp.grid = self.builder.build_map()

        # Events
        self.dragon_events = DragonEvents(self.grid_comp.grid, origin=(sc.OFFSET_X, sc.OFFSET_Y),
                                          tile_size=sc.TILE_SIZE,
                                          damage_heal_popup_manager=self.damage_heal_popup_manager)
        self.tower_events = TowerEvents(self.grid_comp.grid, damage_heal_popup_manager=self.damage_heal_popup_manager)

        # Bannière d'informations
        grid_width = self.grid_comp.grid.nb_columns * self.grid_comp.tile
        self.event_information = BannerInformation(None, x=self.grid_comp.origin[0], y=self.grid_comp.origin[1] - 40,
                                                   width=grid_width,
                                                   height=40)

        self.dragons = []

        # TODO Bouton tour suivant 'temporaire
        self.font = pygame.font.Font(FONT_BUTTON_PATH, 25)
        button_width = 150
        button_height = 50
        button_x = screen.get_width() - button_width - 5
        button_y = screen.get_height() - button_height - 40
        self.next_turn_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        self.button_color = (186, 162, 22)
        self.button_hover_color = (222, 192, 18)
        self.button_text_color = (255, 255, 255)

    def on_gold_change(self, delta):
        self.gold_popup_manager.spawn(*self.ui.coin_position, delta)

    def run_game(self):
        global buy_buttons
        running = True

        while running:
            # Dessiner le jeu
            self.screen.fill(WHITE)
            self.ui.draw(self.screen, current_player=self.turn.current_player())

            # Grille et map
            self.grid_comp.draw(self.screen)
            self.builder.base1.draw(self.screen)
            self.builder.tower1.draw(self.screen)
            self.builder.base2.draw(self.screen)
            self.builder.tower2.draw(self.screen)
            if self.builder.volcano:
                self.builder.volcano.draw(self.screen)
            if self.builder.life_island:
                self.builder.life_island.draw(self.screen)
            if self.builder.tornado and self.builder.tornado.active:
                self.builder.tornado.update(self.grid_comp.grid)
                self.builder.tornado.draw(self.screen)

            # Dessine les bourses pour chaque cellule en parcourant la grille
            for row in self.grid_comp.grid.cells:
                for cell in row:
                    for occupant in cell.occupants:
                        if TypeEntitiesEnum.PLAYER_EFFECT_ZONE in occupant.type_entity:
                            if hasattr(occupant, 'update'):
                                occupant.update()
                            occupant.draw(self.screen)

            # Events
            self.dragon_events.draw(self.screen)
            self.tower_events.draw(self.screen)

            for event in pygame.event.get():
                action = self.ui.handle_event(event)

                if action == "pause":
                    return "pause"
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # obligée de mettre l'appel à towerevents ici sinon ça ne passe pas si on clique sur attaquer
                    if self.tower_events.attack_button_rect and self.tower_events.attack_button_rect.collidepoint(
                            event.pos):
                        self.tower_events.handle_click(event.pos, None, self.turn.current_player(), self.turn)
                        continue

                    # Clic sur le bouton tour suivant (temporaire)
                    if self.next_turn_button_rect.collidepoint(event.pos):
                        if not self.turn.animations_ended(self.builder.tornado):
                            print("Vous devez attendre la fin de toutes les actions avant de passer au tour suivant")
                            continue

                        print("tour de ", self.turn.current_player().name, "terminé")
                        self.turn.next()

                        # reinitialiser toutes les actions des dragons du joueur
                        for dragon in self.turn.current_player().units:
                            dragon.reset_actions()

                        # Appliquer ou retirer les effets des zones sur les dragons
                        for row in self.grid_comp.grid.cells:
                            for cell in row:
                                cell.apply_zone_effects_end_turn(self.damage_heal_popup_manager)

                        # Spawn de la bourse
                        spawn_random_purse(self.grid_comp.grid)

                        # Spawn de la tornade
                        if self.builder.tornado:
                            self.builder.tornado.handle_turn(self.grid_comp.grid)

                        player = self.turn.current_player()
                        player.economy.start_turn()
                        self.turn_popup.show(player.name)
                        print("tour de ", self.turn.current_player().name, "commencé")
                        continue

                    # ouverture et fermeture des panneaux
                    if hasattr(self, 'left_button_rect') and self.left_button_rect.collidepoint(event.pos):
                        self.left_open = not self.left_open
                        continue
                    if hasattr(self, 'right_button_rect') and self.right_button_rect.collidepoint(event.pos):
                        self.right_open = not self.right_open
                        continue

                    # Gestion de l'apparition des bourses

                    # TODO : refactoriser ca
                    clicked_buy_button = False
                    if hasattr(self, 'buy_buttons'):
                        for button in self.buy_buttons:
                            if button["rect"].collidepoint(event.pos):
                                if button["can_afford"]:
                                    remaining_gold = player.economy.get_gold()

                                    # Achat tour de défense
                                    if isinstance(button["dragon"], Tower):
                                        if self.turn.current_player() == self.p1:
                                            self.builder.tower1.tower_activation(self.grid_comp.grid, player,
                                                                                 popup_manager=self.damage_heal_popup_manager)
                                            print("Tour 1 activée", self.builder.tower1.sprite_path)
                                        else:
                                            self.builder.tower2.tower_activation(self.grid_comp.grid, player,
                                                                                 popup_manager=self.damage_heal_popup_manager)
                                        player.economy.spend_gold(button["cost"])
                                        self.event_information.show(TypeEventEnum.NOUVELLE_TOUR)


                                    else:  # Achat dragons
                                        if self.turn.current_player() == self.p1:
                                            spawn_pos = SPAWN_POS_P1
                                        else:
                                            spawn_pos = SPAWN_POS_P2

                                        if self.grid_comp.grid.cells[spawn_pos[1]][spawn_pos[0]].occupants == []:

                                            # Créer une instance du dragon aux coordonnées (0, 0)
                                            dragon_class = button["dragon"].__class__
                                            new_dragon = dragon_class(spawn_pos[0], spawn_pos[1],
                                                                      player=self.turn.current_player())

                                            # Si le dragon est a p2, sa base est en bas a droite -> il doit donc être orienté vers la gauche
                                            if self.turn.current_player() == self.p2:
                                                new_dragon.update_direction("gauche")

                                            self.dragons.append(new_dragon)

                                            # ajoute le dragon a la grille
                                            cell = self.grid_comp.grid.cells[spawn_pos[1]][spawn_pos[0]]
                                            self.grid_comp.grid.add_occupant(new_dragon, cell)

                                            # ajoute le dragon a la liste du joueur
                                            player.add_unit(new_dragon)

                                            player.economy.spend_gold(button["cost"])
                                            self.event_information.show(TypeEventEnum.NOUVEAU_DRAGON)

                                            # logs
                                            print(f"{button['name']} acheté ! argent restant : {remaining_gold}")
                                            print(f"inventaire de dragons : {[d.name for d in self.dragons]}")
                                        else:
                                            print("Impossible d'acheter : la case de spawn est occupée.")
                                else:
                                    print("Impossible d'acheter : fonds insuffisants.")
                                clicked_buy_button = True

                    if not clicked_buy_button:

                        cell = self.grid_comp.handle_click(event.pos)
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

                        if self.dragon_events.selected_dragon is not None:
                            self.dragon_events.handle_click(event.pos, occ, self.turn.current_player(), self.turn)
                        else:
                            if occ and TypeEntitiesEnum.DRAGON in occ.type_entity:
                                self.dragon_events.handle_click(event.pos, occ, self.turn.current_player(), self.turn)

                            elif occ and TypeEntitiesEnum.TOWER in occ.type_entity:
                                self.tower_events.handle_click(event.pos, occ, self.turn.current_player(), self.turn)

                            else:
                                self.dragon_events.handle_click(event.pos, None, self.turn.current_player(), self.turn)

            # ======================================================================================

            # Supprimer les dragons morts de la grille
            for row in self.grid_comp.grid.cells:
                for cell in row:
                    for occupant in cell.occupants:
                        if TypeEntitiesEnum.DRAGON in occupant.type_entity:
                            if occupant.is_dead():
                                print("Dragon mort détecté :", occupant.name)
                                occupant.grant_rewards()
                                occupant.update()
                                cell.remove_occupant(occupant)
                                if occupant.player == self.turn.current_player():
                                    self.event_information.show(TypeEventEnum.MORT_ALLIE)
                                if occupant.player != self.turn.current_player():
                                    self.event_information.show(TypeEventEnum.MORT_ADVERSAIRE)
                            else:
                                occupant.draw(self.screen)
                                occupant.update()
                        if TypeEntitiesEnum.TOWER in occupant.type_entity:
                            if occupant.is_dead():
                                print("Tour morte détectée :", occupant.name)
                                occupant.grant_rewards()
                                occupant.tower_disable(self.grid_comp.grid)
                                self.event_information.show(TypeEventEnum.TOUR_DETRUITE)

            # Gestion base détruite
            if self.builder.base1.is_dead():
                self.event_information.show(TypeEventEnum.BASE_DETRUITE)
                return ("endGame", self.p1.name)
            if self.builder.base2.is_dead():
                self.event_information.show(TypeEventEnum.BASE_DETRUITE)
                return ("endGame", self.p2.name)
            # ======================================================================================

            # Dessiner les side panels et récupérer leurs rectangles (ils doivent être dessinés APRES les dragons)
            player = self.turn.current_player()
            self.left_button_rect, self.right_button_rect, self.current_left_x, self.current_right_x, self.buy_buttons = draw_sidepanels(
                self.screen, self.left_open, self.right_open, self.current_left_x, self.current_right_x, player.economy,
                player)

            # Dessiner le bouton tour suivant (temporaire)
            mouse_pos = pygame.mouse.get_pos()

            # Verifier si toutes les actions sont terminees (dragons ET tornade)
            actions_finished = self.turn.animations_ended(self.builder.tornado)

            # Determiner la couleur du bouton selon l'etat des actions
            if not actions_finished:
                # grisé
                button_color_to_use = (150, 150, 150)
            else:
                # actif
                button_color_to_use = self.button_hover_color if self.next_turn_button_rect.collidepoint(
                    mouse_pos) else self.button_color

            pygame.draw.rect(self.screen, button_color_to_use, self.next_turn_button_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.next_turn_button_rect, 2)
            button_text = self.font.render("Tour suivant", True, self.button_text_color)
            text_rect = button_text.get_rect(center=self.next_turn_button_rect.center)
            self.screen.blit(button_text, text_rect)

            # Afficher le tour du joueur actuel (temporaire)
            turn_text = self.font.render(f"tour de {player.name}", True, (0, 0, 0))
            turn_text_rect = turn_text.get_rect(
                center=(self.next_turn_button_rect.centerx, self.next_turn_button_rect.top - 30))
            self.screen.blit(turn_text, turn_text_rect)

            # Dessiner le popup de tour
            self.turn_popup.draw(self.screen)

            self.event_information.draw(self.screen)

            self.damage_heal_popup_manager.update_and_draw(self.screen)
            self.gold_popup_manager.update_and_draw(self.screen)

            pygame.display.flip()

        return None
