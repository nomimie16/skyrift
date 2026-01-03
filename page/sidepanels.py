#####################
# ONGLET SIDEPANELS #
#####################
import math

import pygame

from component.entities.dragon import Dragonnet, DragonMoyen, DragonGeant
from component.entities.tower import Tower
from player import Player

# Données des dragons
DRAGONS_DATA = [
    Dragonnet,
    DragonMoyen,
    DragonGeant
]

TOWERS_DATA = [
    Tower
]

# cache pour les ressources afin de ne les charger qu'une seule fois depuis le disque
cache = {}


def get_cache(current_player: Player):
    """Charge et met en cache les ressources une seule fois pour optimiser les performances du panneau"""
    if not cache:
        # polices
        cache['font_title'] = pygame.font.Font("assets/font/BoldPixels.ttf", 24)
        cache['font_small'] = pygame.font.Font("assets/font/BoldPixels.ttf", 18)
        cache['font_tiny'] = pygame.font.Font("assets/font/BoldPixels.ttf", 16)

        # icones
        try:
            stat_icon = pygame.image.load("assets/img/HP_icon.png").convert_alpha()
            cache['stat_icon'] = pygame.transform.scale(stat_icon, (12, 12))
        except Exception as e:
            print(f"Erreur chargement icone stat: {e}")
            cache['stat_icon'] = None

        # piece
        try:
            gold_icon = pygame.image.load("assets/img/coin.png").convert_alpha()
            cache['gold_icon'] = pygame.transform.scale(gold_icon, (15, 15))
        except Exception as e:
            print(f"Erreur chargement icone or: {e}")
            cache['gold_icon'] = None

        # fleches pour les boutons de deploiement
        try:
            right_arrow_icon = pygame.image.load("assets/img/right-arrow.png").convert_alpha()
            cache['right_arrow_icon'] = pygame.transform.scale(right_arrow_icon, (20, 20))
        except Exception as e:
            print(f"Erreur chargement fleche droite: {e}")
            cache['right_arrow_icon'] = None

        try:
            left_arrow_icon = pygame.image.load("assets/img/left-arrow.png").convert_alpha()
            cache['left_arrow_icon'] = pygame.transform.scale(left_arrow_icon, (20, 20))
        except Exception as e:
            print(f"Erreur chargement fleche gauche: {e}")
            cache['left_arrow_icon'] = None

        # shop_entities (instances boutiques)
        cache['shop_entities'] = ([dragon_class(0, 0, current_player) for dragon_class in DRAGONS_DATA]
                                  + [Tower(0, 0, f"assets/sprites/tour_{current_player.color}.png", current_player)])

    else:
        if cache['shop_entities'][0]._owner != current_player:
            cache['shop_entities'] = ([dragon_class(0, 0, current_player) for dragon_class in DRAGONS_DATA]
                                      + [Tower(0, 0, f"assets/sprites/tour_{current_player.color}.png",
                                               current_player)])

    return cache


def draw_shop(surface, x_offset, y_start, gold, current_player: Player):
    """Dessine la boutique de dragons dans le panneau gauche"""
    # recupere les ressources depuis le cache
    res = get_cache(current_player)
    font_title = res['font_title']
    font_small = res['font_small']
    font_tiny = res['font_tiny']
    stat_icon = res['stat_icon']
    gold_icon = res['gold_icon']
    entities = res['shop_entities']

    panel_width = 200
    y = y_start

    # titre
    title = font_title.render("Boutique", True, (255, 255, 255))
    title_rect = title.get_rect(center=(panel_width // 2, y + title.get_height() // 2))
    surface.blit(title, title_rect)
    y += 35

    # afficher l'or disponible
    gold_text = font_small.render(f"{gold}", True, (255, 215, 0))
    # texte + icone
    space: int = 4
    total_width = gold_text.get_width() + (15 + space)  # largeur icone + espace
    gold_text_x = (panel_width - total_width) // 2
    gold_rect = gold_text.get_rect(left=gold_text_x, top=y)
    surface.blit(gold_text, gold_rect)
    # icone
    if gold_icon:
        coin_x = gold_text_x + gold_text.get_width() + space
        coin_rect = gold_icon.get_rect(left=coin_x, top=y + 2)
        surface.blit(gold_icon, coin_rect)
    y += 30

    buy_buttons = []

    # afficher chaque dragon
    for entity in entities:

        # fond pour chaque dragon
        dragon_bg = pygame.Rect(x_offset + 5, y, 190, 140)
        pygame.draw.rect(surface, (70, 70, 70), dragon_bg)
        pygame.draw.rect(surface, (100, 100, 100), dragon_bg, 2)

        # image du dragon
        if entity.image_sprite:
            surface.blit(entity.image_sprite[0], (x_offset + 15, y + 25))

        # nom du dragon
        name_text = font_small.render(entity.name, True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(x_offset + 95, y + 5 + name_text.get_height() // 2))
        surface.blit(name_text, name_rect)

        # stats
        stats_y = y + 25
        if isinstance(entity, Tower):
            stats = [
                ("HP:", entity.max_hp),
                ("DMG:", entity.attack_damage),
                ("RNG:", entity.attack_range),
            ]
        else:
            stats = [
                ("HP:", entity.max_hp),
                ("DMG:", entity.attack_damage),
                ("RNG:", entity.attack_range),
                ("SPD:", entity.speed_base),
            ]

        value_x = x_offset + 175  # position fixe pour aligner les nombres a droite
        for label, value in stats:
            # afficher l'icone avant chaque stat
            if stat_icon:
                surface.blit(stat_icon, (x_offset + 90, stats_y + 2))
            # afficher le label
            label_text = font_tiny.render(label, True, (200, 200, 200))
            surface.blit(label_text, (x_offset + 105, stats_y))
            # afficher la valeur alignee a droite
            value_text = font_tiny.render(str(value), True, (200, 200, 200))
            value_rect = value_text.get_rect(right=value_x, top=stats_y)
            surface.blit(value_text, value_rect)
            stats_y += 18

        # bouton d'achat
        button_y = y + 105
        button_rect = pygame.Rect(x_offset + 15, button_y, 170, 25)

        # couleur du bouton selon si on peut acheter
        can_afford = gold >= entity.cost

        if isinstance(entity, Tower) and current_player.tower.active:
            can_afford = False

        button_color = (0, 150, 0) if can_afford else (100, 100, 100)
        pygame.draw.rect(surface, button_color, button_rect)
        pygame.draw.rect(surface, (255, 255, 255), button_rect, 2)

        # texte du bouton
        buy_text = font_small.render(f"{entity.cost}", True, (255, 255, 255))
        text_rect = buy_text.get_rect(center=button_rect.center)
        surface.blit(buy_text, text_rect)
        if gold_icon:
            surface.blit(gold_icon, (button_rect.right - 68, button_y + 5))

        # ajouter le bouton à la liste (avec position absolue à l'écran)
        buy_buttons.append({
            "rect": button_rect,
            "name": entity.name,
            "cost": entity.cost,
            "can_afford": can_afford,
            "dragon": entity
        })

        y += 150

    return buy_buttons


def draw_toggle_button(surface, x, y, size, is_open, current_player: Player):
    """Dessine un bouton demi-circulaire qui gere le deploiement du panneau"""
    color = (100, 150, 100) if is_open else (100, 100, 100)

    # On définit deux points afin de ne creer qu'un demi cercle
    points = []
    for angle in range(-90, 91, 5):
        rad = math.radians(angle)
        px = x + size * math.cos(rad)
        py = y + size * math.sin(rad)
        points.append((px, py))
    points.append((x, y))

    if len(points) > 2:
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, (255, 255, 255), points, 2)

    # fleche
    res = get_cache(current_player)
    if is_open:
        arrow_icon = res['left_arrow_icon']
    else:
        arrow_icon = res['right_arrow_icon']

    if arrow_icon:
        arrow_x = x + 8 if is_open else x + 10
        arrow_rect = arrow_icon.get_rect(center=(arrow_x, y))
        surface.blit(arrow_icon, arrow_rect)


def draw_sidepanels(screen, left_open, right_open, current_left_x, current_right_x, economy, current_player: Player):
    panel_width = 200
    screen_height = screen.get_height()
    animation_speed = 8
    button_size = 20
    button_y = screen_height // 2

    # calculer les positions cibles
    target_left_x = 0 if left_open else -panel_width
    target_right_x = screen.get_width() - panel_width if right_open else screen.get_width()

    # animation gauche
    if current_left_x < target_left_x:
        current_left_x = min(current_left_x + animation_speed, target_left_x)
    elif current_left_x > target_left_x:
        current_left_x = max(current_left_x - animation_speed, target_left_x)

    # animation droite
    if current_right_x < target_right_x:
        current_right_x = min(current_right_x + animation_speed, target_right_x)
    elif current_right_x > target_right_x:
        current_right_x = max(current_right_x - animation_speed, target_right_x)

    # onglet gauche avec boutique
    left_rect = pygame.Rect(current_left_x, 0, panel_width, screen_height)
    left_panel = pygame.Surface((panel_width, screen_height))
    left_panel.fill((50, 50, 50))

    # dessiner la boutique
    buy_buttons = []
    gold = economy.get_gold()
    buy_buttons = draw_shop(left_panel, 0, 20, gold, current_player)

    # ajuster les positions des boutons pour l'écran absolu
    for button in buy_buttons:
        button["rect"].x += current_left_x

    screen.blit(left_panel, (current_left_x, 0))

    left_button_x = current_left_x + panel_width
    left_button_rect = pygame.Rect(left_button_x - button_size, button_y - button_size, button_size * 2,
                                   button_size * 2)
    draw_toggle_button(screen, left_button_x, button_y, button_size, left_open, current_player)

    # onglet droit
    right_panel = pygame.Surface((panel_width, screen_height))
    right_panel.fill((50, 50, 50))
    screen.blit(right_panel, (current_right_x, 0))

    # Bouton pour ouvrir/fermer le panneau droit
    right_button_x = current_right_x
    right_button_rect = pygame.Rect(right_button_x - button_size, button_y - button_size, button_size * 2,
                                    button_size * 2)
    draw_toggle_button(screen, right_button_x, button_y, button_size, right_open, current_player)

    return left_button_rect, right_button_rect, current_left_x, current_right_x, buy_buttons
