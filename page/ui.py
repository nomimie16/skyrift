##########################
#MODULE D'INTERFACE COMMUN
##########################

import pygame

class UIOverlay:
    def __init__(self, screen):
        '''Chargement des icons'''
        # Bouton quitter le jeu
        self.quit_img = pygame.image.load("assets/img/quit.png").convert_alpha()
        self.quit_img = pygame.transform.scale(self.quit_img, (55, 55))
        self.quit_rect = self.quit_img.get_rect()
        self.quit_rect.topleft = (screen.get_width() - 50, 0)
        # Bouton settings 
        self.settings_img = pygame.image.load("assets/img/settings.png").convert_alpha()
        self.settings_img = pygame.transform.scale(self.settings_img, (55, 55))
        self.settings_rect = self.settings_img.get_rect()
        self.settings_rect.topleft = (screen.get_width() - 90, 0)
        
    def draw(self, screen):
        '''Fonction dessine les images/icons'''
        screen.blit(self.quit_img, self.quit_rect)
        screen.blit(self.settings_img, self.settings_rect)
        
    def handle_event(self, event):
        '''Retourne une action selon le bouton cliqué'''
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Bouton quitter cliqué
            if self.quit_rect.collidepoint(event.pos):
                print("Jeu SkyRift Fermé.\n")
                return 'quit'
            #Bouton setting cliqué
            if self.settings_rect.collidepoint(event.pos):
                print("Ouverture des paramètres.\n")
                return 'settings'