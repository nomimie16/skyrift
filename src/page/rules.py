########################
# FENETRE REGLE DU JEU #
########################

import pygame
from src.const import *

def run_rules(screen, from_game):

    # Image
    fond = pygame.image.load(IMG_BG_RULES).convert()
    fond = pygame.transform.scale(fond, (screen.get_width(), screen.get_height()))
    
    # Polices
    try:
        FONT_TITLE = pygame.font.Font(FONT_TITLE_PATH, 72)
        FONT_TEXT = pygame.font.Font(FONT_BUTTON_PATH, 36)
    except:
        FONT_TITLE = pygame.font.SysFont(None, 72)
        FONT_TEXT = pygame.font.SysFont(None, 36)
        
    # Contenu des pages
    pages_content = {
        0: {
            "page_gauche": {
                "sections": [
                    {
                        "titre": "Bienvenue",
                        "texte": [
                            "SkyRift est un jeu de",
                            "stratégie où deux joueurs",
                            "s'affrontent dans un monde",
                            "fantastique rempli de",
                            "dragons et de dangers."
                        ]
                    },
                    {
                        "titre": "Objectif",
                        "texte": [
                            "Détruisez la base adverse",
                            "en utilisant vos dragons et",
                            "vos tours de défense tout",
                            "en protégeant la vôtre."
                        ]
                    }
                ]
            },
            "page_droite": {
                "sections": [
                    {
                        "titre": "Les Dragons",
                        "texte": [
                            "Dragonnet : 100 pièces",
                            "Dragon Moyen : 300 pièces",
                            "Dragon Géant : 600 pièces"
                        ]
                    },
                    {
                        "titre": "Les Tours",
                        "texte": [
                            "Les tours de défense",
                            "protègent votre base et",
                            "attaquent automatiquement",
                            "les ennemis à portée."
                        ]
                    }
                ]
            }
        },
        1: {
            "page_gauche": {
                "sections": [
                    {
                        "titre": "Comment jouer",
                        "texte": [
                            "1. Achetez des dragons",
                            "   dans la boutique",
                            "2. Cliquez sur un dragon",
                            "   pour le sélectionner",
                            "3. Déplacez-le en cliquant",
                            "   sur une case adjacente"
                        ]
                    },
                    {
                        "titre": "Actions",
                        "texte": [
                            "Attaquez les ennemis en",
                            "cliquant sur une unité",
                            "adverse à portée, ou",
                            "passez votre tour."
                        ]
                    }
                ]
            },
            "page_droite": {
                "sections": [
                    {
                        "titre": "Economie",
                        "texte": [
                            "Vous gagnez 75 pièces",
                            "d'or à chaque fin de",
                            "tour pour acheter de",
                            "nouvelles unités."
                        ]
                    },
                    {
                        "titre": "Bourses d'or",
                        "texte": [
                            "Des bourses apparaissent",
                            "aléatoirement sur la carte.",
                            "Déplacez un dragon dessus",
                            "pour récupérer de l'or !"
                        ]
                    }
                ]
            }
        },
        2: {
            "page_gauche": {
                "sections": [
                    {
                        "titre": "Evenements",
                        "texte": [
                            "Attention aux dangers",
                            "naturels présents sur",
                            "la carte qui peuvent",
                            "vous aider ou nuire !"
                        ]
                    },
                    {
                        "titre": "Le Volcan",
                        "texte": [
                            "Si votre dragon passe",
                            "sur une case volcanique,",
                            "il perd des points de vie.",
                            "Évitez ces zones !"
                        ]
                    }
                ]
            },
            "page_droite": {
                "sections": [
                    {
                        "titre": "L'Ile de Vie",
                        "texte": [
                            "Les îles de vie soignent",
                            "vos dragons lorsqu'ils",
                            "passent dessus. Utilisez-",
                            "les stratégiquement !"
                        ]
                    },
                    {
                        "titre": "La Tornade",
                        "texte": [
                            "Une tornade se déplace",
                            "aléatoirement sur la carte.",
                            "Si un dragon est sur son",
                            "passage, il subit des",
                            "dégâts importants !"
                        ]
                    }
                ]
            }
        }
    }

    # Variable pour suivre la page actuelle
    current_page = 0
    max_page = len(pages_content) - 1
    
    # Texte "Retour au jeu"
    text = "Retour au jeu"
    text_pos = (screen.get_width() // 2, screen.get_height() - 80)
    
    # Image du fond du bouton
    bgButton = pygame.image.load(IMG_BGBUTTONRULES).convert_alpha()
    bgButton = pygame.transform.scale(bgButton, (400, 150))
    bgButton_rect = bgButton.get_rect(center=text_pos)

    # Image du livre
    livre = pygame.image.load(IMG_LIVRE).convert_alpha()
    livre = pygame.transform.scale(livre, (800, 450))
    livre_rect = livre.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    # Image du livre
    livre = pygame.image.load(IMG_LIVRE).convert_alpha()
    livre = pygame.transform.scale(livre, (800, 450))
    livre_rect = livre.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Flèches pour tourner les pages
    left_arrow = pygame.image.load(IMG_LEFTARROW).convert_alpha()
    left_arrow = pygame.transform.scale(left_arrow, (50, 50))  # Ajustez la taille
    left_arrow_rect = left_arrow.get_rect(midleft=(livre_rect.left + 20, livre_rect.centery))
    right_arrow = pygame.image.load(IMG_RIGHTARROW).convert_alpha()
    right_arrow = pygame.transform.scale(right_arrow, (50, 50))
    right_arrow_rect = right_arrow.get_rect(midright=(livre_rect.right - 20, livre_rect.centery))
            
    # Ecrit le contenu de la page du livre
    def draw_page_content(surface, page_data, livre_rect, font_title, font_text):
        # Page gauce
        left_x = livre_rect.centerx - livre_rect.width // 5
        y_offset = livre_rect.top + 50
        for section in page_data["page_gauche"]["sections"]:
            # Titre
            titre = font_title.render(section["titre"], True, (50, 30, 10))
            titre = pygame.transform.scale(titre, (int(titre.get_width() * 0.35), int(titre.get_height() * 0.35)))
            titre_rect = titre.get_rect(center=(left_x, y_offset))
            surface.blit(titre, titre_rect)
            y_offset += 35
            # Contenu
            for ligne in section["texte"]:
                ligne_surf = font_text.render(ligne, True, (80, 50, 20))
                ligne_surf = pygame.transform.scale(ligne_surf, (int(ligne_surf.get_width() * 0.55), int(ligne_surf.get_height() * 0.55)))
                ligne_rect = ligne_surf.get_rect(center=(left_x, y_offset))
                surface.blit(ligne_surf, ligne_rect)
                y_offset += 22
            # Espace
            y_offset += 15
        
        # Page de droite
        right_x = livre_rect.centerx + livre_rect.width // 5
        y_offset = livre_rect.top + 50
        for section in page_data["page_droite"]["sections"]:
            # Titre
            titre = font_title.render(section["titre"], True, (50, 30, 10))
            titre = pygame.transform.scale(titre, (int(titre.get_width() * 0.35), int(titre.get_height() * 0.35)))
            titre_rect = titre.get_rect(center=(right_x, y_offset))
            surface.blit(titre, titre_rect)
            y_offset += 35
            # Contenu
            for ligne in section["texte"]:
                ligne_surf = font_text.render(ligne, True, (80, 50, 20))
                ligne_surf = pygame.transform.scale(ligne_surf, (int(ligne_surf.get_width() * 0.55), int(ligne_surf.get_height() * 0.55)))
                ligne_rect = ligne_surf.get_rect(center=(right_x, y_offset))
                surface.blit(ligne_surf, ligne_rect)
                y_offset += 22
            # Espace
            y_offset += 15
            
    # === BOUCLE PRINCIPALE ===
    running = True
    while running:
        
        mouse_pos = pygame.mouse.get_pos()

        # Dessiner le jeu
        screen.blit(fond, (0, 0))
        
        # Titre
        title = FONT_TITLE.render("Regles du jeu", True, WHITE)
        shadow = FONT_TITLE.render("Regles du jeu", True, SHADOW)
        screen.blit(shadow, (screen.get_width() // 2 - title.get_width() // 2 + 3, 103))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))

        # Txt back to game
        color = TRANSLUCENT_BLUE if bgButton_rect.collidepoint(mouse_pos) else (147, 96, 36, 0.8)
        text_surface = FONT_TEXT.render(text, True, color)
        text_rect = text_surface.get_rect(center=text_pos)

        # Dessiner le bouton retour
        screen.blit(bgButton, bgButton_rect)
        screen.blit(text_surface, text_rect)
        
        # Dessiner le livre
        screen.blit(livre, livre_rect)
        
        # Griser la flèche gauche si on est à la première page
        if current_page == 0:
            left_arrow.set_alpha(100)
        else:
            left_arrow.set_alpha(255)

        # Griser la flèche droite si on est à la dernière page
        if current_page == max_page:
            right_arrow.set_alpha(100)
        else:
            right_arrow.set_alpha(255)

        # Dessiner les flèches
        screen.blit(left_arrow, left_arrow_rect)
        screen.blit(right_arrow, right_arrow_rect)
        
        # Dessiner le texte du livre
        draw_page_content(screen, pages_content[current_page], livre_rect, FONT_TITLE, FONT_TEXT)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if bgButton_rect.collidepoint(event.pos):
                    return 'game' if from_game else 'startGame'

                # page précédente
                if left_arrow_rect.collidepoint(event.pos):
                    if current_page > 0:
                        current_page -= 1
                        print(f"Page {current_page}")

                # page suivante
                if right_arrow_rect.collidepoint(event.pos):
                    if current_page < max_page:
                        current_page += 1
                        print(f"Page {current_page}")
                
        pygame.display.flip()

    return None