########################
# FENETRE DEBUT DU JEU #
########################

from pygame import *
import pygame
import contants_graph

def run_start(screen):
    
    #Taille de l'écran
    WIDTH = screen.get_width()  
    
    #Images
    fond = contants_graph.startBackground
    fond = fond.convert()
    
    #Musique
    #mixer.music.load('assets/sound/startMusic.mp3')
    #mixer.music.play(-1)

    # ==== CLASSE BOUTONS ======
    class Button:
        def __init__(self, text, center_y, action):
            
            self.text = text
            self.action = action
            self.center_y = center_y
            self.width, self.height = 320, 70
            self.rect = pygame.Rect((0,0, self.width, self.height))
            self.rect.center = (WIDTH//2, center_y)
            
        def draw(self, win, mouse_pos):
            is_hover = self.rect.collidepoint(mouse_pos)
            color = contants_graph.HOVER_BLUE if is_hover else contants_graph.TRANSLUCENT_BLUE
            button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(button_surface, color, (0,0,self.width, self.height), border_radius = 16)
            win.blit(button_surface, self.rect)
            
            text_surf = contants_graph.FONT_BUTTON.render(self.text, True, contants_graph.WHITE)
            text_rect = text_surf.get_rect(center=self.rect.center)
            
            shadow = contants_graph.FONT_BUTTON.render(self.text, True, contants_graph.SHADOW)
            win.blit(shadow, (text_rect.x+2, text_rect.y+2))
            win.blit(text_surf, text_rect)
        
        def is_clicked(self, mouse_pos, mouse_pressed):
            return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]
    
    # ===== BOUTONS =====
    buttons = [
        Button("Lancer le jeu", 320, "game"),
        Button("Options", 420, "settingsFromStart"),
        Button("Règles", 520, "rulesFromStart"),
        Button("Quitter", 620, "quit")
    ]     


    # ===== BOUCLE PRINCIPALE =====
    running = True
    while running:
        
        # Boucle d'événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("\nFermeture du jeu.")
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        print(f"Action : {button.action}")
                        return button.action
        
        screen.blit(fond, (0,0))
        mouse_pos = pygame.mouse.get_pos()
        
        #Titre
        title = contants_graph.FONT_TITLE.render("SkyRift", True, contants_graph.WHITE)
        shadow = contants_graph.FONT_TITLE.render("SkyRift", True, contants_graph.SHADOW)
        screen.blit(shadow, (WIDTH//2 - title.get_width()//2 +3, 103))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))        
    
        for button in buttons:
            button.draw(screen, mouse_pos)
                    
        pygame.display.flip()

    return None