#####################
# ONGLET SIDEPANELS #
#####################
import math
import pygame

import src.screen_const as sc
from src.component.entities.dragon import Dragonnet, DragonMoyen, DragonGeant
from src.component.entities.tower import Tower
from src.const import IMG_BGSIDEPANEL, IMG_SORCIER, IMG_BANDEAU
from src.player import Player
from src.page.component.base_panel import BasePanel

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
        cache['font_title'] = pygame.font.Font("src/assets/font/BoldPixels.ttf", 24)
        cache['font_small'] = pygame.font.Font("src/assets/font/BoldPixels.ttf", 22)
        cache['font_tiny'] = pygame.font.Font("src/assets/font/BoldPixels.ttf", 16)

        # icones
        try:
            stat_icon = pygame.image.load("src/assets/img/HP_icon.png").convert_alpha()
            cache['stat_icon'] = pygame.transform.scale(stat_icon, (12, 12))
        except Exception as e:
            print(f"Erreur chargement icone stat: {e}")
            cache['stat_icon'] = None

        # piece
        try:
            gold_icon = pygame.image.load("src/assets/img/coin.png").convert_alpha()
            cache['gold_icon'] = pygame.transform.scale(gold_icon, (15, 15))
        except Exception as e:
            print(f"Erreur chargement icone or: {e}")
            cache['gold_icon'] = None

        # fleches pour les boutons de deploiement
        try:
            right_arrow_icon = pygame.image.load("src/assets/img/right-arrow.png").convert_alpha()
            cache['right_arrow_icon'] = pygame.transform.scale(right_arrow_icon, (20, 20))
        except Exception as e:
            print(f"Erreur chargement fleche droite: {e}")
            cache['right_arrow_icon'] = None

        try:
            left_arrow_icon = pygame.image.load("src/assets/img/left-arrow.png").convert_alpha()
            cache['left_arrow_icon'] = pygame.transform.scale(left_arrow_icon, (20, 20))
        except Exception as e:
            print(f"Erreur chargement fleche gauche: {e}")
            cache['left_arrow_icon'] = None

        # images shop
        try:
            bg_image = pygame.image.load(IMG_BGSIDEPANEL).convert()
            cache['bg_image'] = pygame.transform.scale(bg_image, (sc.PANEL_WIDTH, sc.SCREEN_H))
        except Exception as e:
            print(f"Erreur chargement image fond shop: {e}")
            cache['bg_image'] = None

        try:
            bg_sorcier = pygame.image.load(IMG_SORCIER).convert_alpha()
            cache['bg_sorcier'] = pygame.transform.scale(bg_sorcier, (200, 200))
        except Exception as e:
            print(f"Erreur chargement image sorcier: {e}")
            cache['bg_sorcier'] = None
            
        try:
            img_bandeau = pygame.image.load(IMG_BANDEAU).convert_alpha()
            cache['img_bandeau'] = pygame.transform.scale(img_bandeau, (35, sc.SCREEN_H))
        except Exception as e:
            print(f"Erreur chargement image bandeau shop: {e}")
            cache['img_bandeau'] = None

        # shop_entities (instances boutiques)
        cache['shop_entities'] = ([dragon_class(0, 0, current_player) for dragon_class in DRAGONS_DATA]
                                  + [Tower(0, 0, f"src/assets/sprites/tour_{current_player.color}.png",
                                           current_player)])

        # redimenstionnement
        cache['shop_entity_sprites'] = {}
        img_size = int(sc.PANEL_WIDTH * 0.35)
        for entity in cache['shop_entities']:
            if entity.image_sprite:
                img = entity.image_sprite[0]
                if isinstance(entity, Tower):
                    shop_size = int(img_size * 0.7), img_size
                else:
                    shop_size = (img_size, img_size)
                cache['shop_entity_sprites'][entity.name] = pygame.transform.smoothscale(img, shop_size)

        if cache['gold_icon']:
            card_width = sc.PANEL_WIDTH - (int(sc.PANEL_WIDTH * 0.05) * 2)
            card_height = int(card_width * 0.75)
            btn_height = int(card_height * 0.15)
            small_coin_size = int(btn_height * 0.6)
            cache['small_gold_icon'] = pygame.transform.smoothscale(cache['gold_icon'], (small_coin_size, small_coin_size))

    else:
        if cache['shop_entities'][0].player != current_player:
            cache['shop_entities'] = ([dragon_class(0, 0, current_player) for dragon_class in DRAGONS_DATA]
                                      + [Tower(0, 0, f"src/assets/sprites/tour_{current_player.color}.png",
                                               current_player)])

            cache['shop_entity_sprites'] = {}
            img_size = int(sc.PANEL_WIDTH * 0.35)
            for entity in cache['shop_entities']:
                if entity.image_sprite:
                    img = entity.image_sprite[0]
                    if isinstance(entity, Tower):
                        shop_size = int(img_size * 0.7), img_size
                    else:
                        shop_size = (img_size, img_size)
                    cache['shop_entity_sprites'][entity.name] = pygame.transform.smoothscale(img, shop_size)

    return cache


def draw_shop(surface, x_offset, y_start, gold, current_player: Player, panel_width: int):
    """Dessine la boutique de dragons dans le panneau gauche"""
    # recupere les ressources depuis le cache
    res = get_cache(current_player)
    # font_title = res['font_title']
    font_small = res['font_small']
    font_tiny = res['font_tiny']
    stat_icon = res['stat_icon']
    # gold_icon = res['gold_icon']
    entities = res['shop_entities']

    card_margin = int(panel_width * 0.05)
    card_width = panel_width - (card_margin * 2)
    card_height = int(card_width * 0.75)

    spacing_y = int(card_height * 1.1)

    y = y_start
    center_x = x_offset + panel_width // 2

    # # titre
    # title = font_title.render("Boutique", True, (255, 255, 255))
    # title_rect = title.get_rect(center=(center_x, y + title.get_height() // 2))
    # surface.blit(title, title_rect)
    # y += int(panel_width * 0.18)

    # # afficher l'or disponible
    # gold_text = font_small.render(f"{gold}", True, (255, 215, 0))
    # # texte + icone
    # space: int = int(panel_width * 0.02)
    # total_width = gold_text.get_width() + (gold_icon.get_width() + space if gold_icon else 0)

    # gold_text_x = x_offset + (panel_width - total_width) // 2
    # gold_rect = gold_text.get_rect(left=gold_text_x, top=y)
    # surface.blit(gold_text, gold_rect)
    # icone
    # if gold_icon:
    #     surface.blit(gold_icon, (gold_text_x + gold_text.get_width() + space, y))

    # y += int(panel_width * 0.15)

    buy_buttons = []

    # afficher chaque dragon
    for entity in entities:
        card_x = x_offset + card_margin

        # Cadre style bois
        card_panel = BasePanel(card_width, card_x, y, card_height)
        card_panel._draw_wood_frame(surface)
        corner_size = 8
        line_y = y + 3
        for _ in range(3):
            pygame.draw.line(surface, BasePanel.WOOD_DARK, 
                            (card_x + corner_size, line_y),
                            (card_x + card_width - corner_size, line_y), 1)
            line_y += 1

        line_y = y + card_height - 6
        for _ in range(3):
            pygame.draw.line(surface, BasePanel.WOOD_DARK,
                            (card_x + corner_size, line_y),
                            (card_x + card_width - corner_size, line_y), 1)
            line_y += 1

        # image de l'entité (taille boutique)
        cached_sprites = res.get('shop_entity_sprites', {})
        if entity.name in cached_sprites:
            img_shop = cached_sprites[entity.name]
            img_x = card_x + int(card_width * 0.05)
            img_y = y + (card_height - img_shop.get_height()) // 2
            surface.blit(img_shop, (img_x, img_y))

        # nom du dragon
        name_text = font_small.render(entity.name, True, BasePanel.WOOD_DARK)
        right_area_x = card_x + int(card_width * 0.45)
        right_area_w = int(card_width * 0.55)

        name_rect = name_text.get_rect(center=(card_x + card_width // 2, y + 25))
        surface.blit(name_text, name_rect)

        # stats
        stats_y = y + int(card_height * 0.28)
        line_height = int(card_height * 0.13)

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

        stat_x_label = right_area_x + int(right_area_w * 0.2)
        stat_x_val = card_x + card_width - int(card_width * 0.1)

        current_stat_y = stats_y

        for label, value in stats:
            # afficher l'icone avant chaque stat
            if stat_icon:
                surface.blit(stat_icon, (stat_x_label - stat_icon.get_width() - 2, current_stat_y + 2))
            # afficher le label
            label_text = font_tiny.render(label, True, BasePanel.WOOD_MEDIUM)
            surface.blit(label_text, (stat_x_label, current_stat_y))
            # afficher la valeur alignee a droite
            value_text = font_tiny.render(str(value), True, BasePanel.WOOD_LIGHT)
            value_rect = value_text.get_rect(right=stat_x_val, top=current_stat_y)
            surface.blit(value_text, value_rect)
            current_stat_y += line_height

        # bouton d'achat
        btn_height = int(card_height * 0.15)
        btn_width = int(card_width * 0.9)
        btn_x = card_x + (card_width - btn_width) // 2
        btn_y = y + card_height - btn_height - int(card_height * 0.05)

        button_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)

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
        small_coin = res.get('small_gold_icon')
        if small_coin:
            surface.blit(small_coin, (text_rect.right + 5, btn_y + (btn_height - small_coin.get_height()) // 2))

        # ajouter le bouton à la liste (avec position absolue à l'écran)
        buy_buttons.append({
            "rect": button_rect,
            "name": entity.name,
            "cost": entity.cost,
            "can_afford": can_afford,
            "dragon": entity
        })

        y += spacing_y

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
    
    panel_width = sc.PANEL_WIDTH
    screen_height = screen.get_height()
    animation_speed = 20
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

    res = get_cache(current_player)
    if res['bg_image']:
        left_panel.blit(res['bg_image'], (0, 0))

    # dessiner la boutique
    buy_buttons = []
    gold = economy.get_gold()
    buy_buttons = draw_shop(left_panel, 0, 20, gold, current_player, panel_width)

    if res['bg_sorcier']:
        left_panel.blit(res['bg_sorcier'], (0, screen_height - 200))

    # ajuster les positions des boutons pour l'écran absolu
    for button in buy_buttons:
        button["rect"].x += current_left_x

    screen.blit(left_panel, (current_left_x, 0))

    # bandeau "magasin"
    if res['img_bandeau']:
        bandeau_x = current_left_x + panel_width
        screen.blit(res['img_bandeau'], (bandeau_x, 0))

    left_button_x = current_left_x + panel_width + 35
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
