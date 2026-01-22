############################
# MODULE D'INTERFACE COMMUN #
############################

import pygame

from src.const import *
from src.player import Player


class UIOverlay:
    def __init__(self, screen):
        '''Chargement des icons'''
        # Bouton pause
        self.pause_btn = pygame.image.load("src/assets/img/pause_button.png").convert_alpha()
        self.pause_btn = pygame.transform.scale(self.pause_btn, (55, 55))
        self.pause_rect = self.pause_btn.get_rect()
        self.pause_rect.topright = (screen.get_width() - 10, 0)

        # Monnaie
        self.coin_img = pygame.image.load("src/assets/img/coin.png").convert_alpha()
        self.coin_img = pygame.transform.scale(self.coin_img, (50, 50))
        self.coin_rect = self.coin_img.get_rect()
        self.coin_rect.topleft = (10, 10)
        self.coin_value = 0
        self.coin_text = pygame.font.Font(FONT_TITLE_PATH, 50).render(str(self.coin_value), True, (255, 215, 0))
        self.coin_text_rect = self.coin_text.get_rect()
        self.coin_text_rect.topleft = (70, 20)
        self.coin_font = pygame.font.Font(FONT_TITLE_PATH, 50)
        self.coin_position = (
            self.coin_text_rect.right + 10,
            self.coin_text_rect.centery
        )

        # Joueur en cours
        self.current_player = pygame.font.Font(FONT_BUTTON_PATH, 36).render("Joueur 1", True, (0, 0, 0))
        self.current_player_rect = self.current_player.get_rect(center=(screen.get_width() // 2, 35))
        self.player_font = pygame.font.Font(FONT_BUTTON_PATH, 36)

    def draw(self, screen, current_player: Player):
        '''Fonction dessine les images/icons'''
        screen.blit(self.pause_btn, self.pause_rect)
        screen.blit(self.coin_img, self.coin_rect)

        if current_player:
            self.current_player = self.player_font.render(f"Tour de {current_player.name}", True, (0, 0, 0))
            self.current_player_rect = self.current_player.get_rect(center=(screen.get_width() // 2, 35))

            self.coin_value = current_player.economy.get_gold()
            self.coin_text = self.coin_font.render(str(self.coin_value), True, (255, 215, 0))
            self.coin_text_rect = self.coin_text.get_rect()
            self.coin_text_rect.topleft = (70, 20)

            self.coin_position = (
                self.coin_text_rect.right + 10,
                self.coin_text_rect.centery
            )
        screen.blit(self.coin_text, self.coin_text_rect)
        screen.blit(self.current_player, self.current_player_rect)

    def handle_event(self, event):
        '''Retourne une action selon le bouton cliqué'''
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Bouton pause cliqué
            if self.pause_rect.collidepoint(event.pos):
                return 'pause'
