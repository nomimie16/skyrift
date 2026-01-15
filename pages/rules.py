########################
# FENETRE REGLE DU JEU #
########################

from calendar import c
from tkinter import W
from pygame import *
import pygame
import contants_graph


def run_rules(screen, from_game):
    WHITE = contants_graph.WHITE
    TRANSLUCENT_RED = contants_graph.TRANSLUCENT_RED
    HOVER_RED = contants_graph.HOVER_RED
    SHADOW = contants_graph.SHADOW
    fond = contants_graph.rulesBackground
    fond = fond.convert()
    FONT_TITLE = contants_graph.FONT_TITLE
    FONT_BUTTON = contants_graph.FONT_BUTTON
       
    #Musique
    #mixer.music.load('assets/sound/startMusic.mp3')
    #mixer.music.play(-1)

    # ==== BOUTON ======
    btn_retour = pygame.Rect(
        screen.get_width() // 2- 100,
        screen.get_height() // 2 + 300,
        200,
        60
    )
       

    # === BOUCLE PRINCIPALE ===
    running = True
    while running:
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Dessiner le jeu
        screen.blit(fond, (0,0))

        
        is_hover = btn_retour.collidepoint(mouse_pos)
        color = HOVER_RED if is_hover else TRANSLUCENT_RED
        button_surface = pygame.Surface((btn_retour.width, btn_retour.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, color, (0,0,btn_retour.width, btn_retour.height), border_radius = 16)
        screen.blit(button_surface, btn_retour)
        text = FONT_BUTTON.render("Retour", True, WHITE)
        text_rect = text.get_rect(center=btn_retour.center)
        screen.blit(text, text_rect)

        
        title = FONT_TITLE.render("Regles du jeu", True, WHITE)
        shadow = FONT_TITLE.render("Regles du jeu", True, SHADOW)
        screen.blit(shadow, (screen.get_width()//2 - title.get_width()//2 +3, 103))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 100))     
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retour.collidepoint(event.pos):
                    if from_game:
                        return 'game'
                    else:
                        return 'startGame'

                    
        pygame.display.flip()

    return None