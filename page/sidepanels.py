#####################
# ONGLET SIDEPANELS #
#####################
import pygame
from component.entities.dragon import Dragonnet, DragonMoyen, DragonGeant

# Charger les sprites des dragons pour la boutique
try:
    dragonnet_img = pygame.image.load("assets\sprites\dragonnet_test.png").convert_alpha()
    dragonnet_img = pygame.transform.scale(dragonnet_img, (50, 50))
except:
    dragonnet_img = None

try:
    dragon_moyen_img = pygame.image.load("assets/sprites/dragonnet_test.png").convert_alpha()
    dragon_moyen_img = pygame.transform.scale(dragon_moyen_img, (50, 50))
except:
    dragon_moyen_img = None

try:
    dragon_geant_img = pygame.image.load("assets/sprites/dragonnet_test.png").convert_alpha()
    dragon_geant_img = pygame.transform.scale(dragon_geant_img, (50, 50))
except:
    dragon_geant_img = None

# Données des dragons
DRAGONS_DATA = [
    Dragonnet,
    DragonMoyen,
    DragonGeant
]

# cache pour les ressources afin de ne les charger qu'une seule fois depuis le disque
cache = {}

def get_cache():
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

        # dragon (instances boutiques)
        cache['dragons'] = [dragon_class(0, 0) for dragon_class in DRAGONS_DATA]

    return cache

def draw_shop(surface, x_offset, y_start, gold):
    """Dessine la boutique de dragons dans le panneau gauche"""
    # recupere les ressources depuis le cache
    res = get_cache()
    font_title = res['font_title']
    font_small = res['font_small']
    font_tiny = res['font_tiny']
    stat_icon = res['stat_icon']
    gold_icon = res['gold_icon']
    dragons = res['dragons']

    panel_width = 200
    y = y_start

    # titre
    title = font_title.render("Boutique", True, (255, 255, 255))
    title_rect = title.get_rect(center=(panel_width // 2, y + title.get_height() // 2))
    surface.blit(title, title_rect)
    y += 35

    # afficher l'or disponible
    gold_text = font_small.render(f"Gold: {gold}", True, (255, 215, 0))
    gold_rect = gold_text.get_rect(center=(panel_width // 2, y + gold_text.get_height() // 2))
    surface.blit(gold_text, gold_rect)
    y += 30

    buy_buttons = []

    # afficher chaque dragon
    for dragon in dragons:

        # fond pour chaque dragon
        dragon_bg = pygame.Rect(x_offset + 5, y, 190, 140)
        pygame.draw.rect(surface, (70, 70, 70), dragon_bg)
        pygame.draw.rect(surface, (100, 100, 100), dragon_bg, 2)

        # Image du dragon
        if dragon.image_sprite:
            surface.blit(dragon.image_sprite[0], (x_offset + 15, y + 25))

        # Nom du dragon
        name_text = font_small.render(dragon.name, True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(x_offset + 95, y + 5 + name_text.get_height() // 2))
        surface.blit(name_text, name_rect)

        # Stats
        stats_y = y + 25
        stats = [
            ("HP:", dragon.max_hp),
            ("DMG:", dragon.attack_damage),
            ("RNG:", dragon.attack_range),
            ("SPD:", dragon.base_speed)
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

        # Bouton d'achat
        button_y = y + 105
        button_rect = pygame.Rect(x_offset + 15, button_y, 170, 25)

        # Couleur du bouton selon si on peut acheter
        can_afford = gold >= dragon.cost
        button_color = (0, 150, 0) if can_afford else (100, 100, 100)
        pygame.draw.rect(surface, button_color, button_rect)
        pygame.draw.rect(surface, (255, 255, 255), button_rect, 2)

        # Texte du bouton
        buy_text = font_small.render(f"{dragon.cost}", True, (255, 255, 255))
        text_rect = buy_text.get_rect(center=button_rect.center)
        surface.blit(buy_text, text_rect)
        if gold_icon:
            surface.blit(gold_icon, (button_rect.right - 68, button_y + 5))

        # Ajouter le bouton à la liste (avec position absolue à l'écran)
        buy_buttons.append({
            "rect": button_rect,
            "name": dragon.name,
            "cost": dragon.cost,
            "can_afford": can_afford,
            "dragon": dragon
        })

        y += 150

    return buy_buttons

def draw_sidepanels(screen, left_open, right_open, current_left_x, current_right_x, economy=None):
    panel_width = 200
    screen_height = screen.get_height()
    animation_speed = 8

    # Calculer les positions cibles
    target_left_x = 0 if left_open else -panel_width + 20
    target_right_x = screen.get_width() - panel_width if right_open else screen.get_width() - 20

    # Animation gauche
    if current_left_x < target_left_x:
        current_left_x = min(current_left_x + animation_speed, target_left_x)
    elif current_left_x > target_left_x:
        current_left_x = max(current_left_x - animation_speed, target_left_x)

    # Animation droite
    if current_right_x < target_right_x:
        current_right_x = min(current_right_x + animation_speed, target_right_x)
    elif current_right_x > target_right_x:
        current_right_x = max(current_right_x - animation_speed, target_right_x)

    # Onglet gauche avec boutique
    left_rect = pygame.Rect(current_left_x, 0, panel_width, screen_height)
    left_panel = pygame.Surface((panel_width, screen_height))
    left_panel.fill((50, 50, 50))

    # Dessiner la boutique si l'économie est fournie
    buy_buttons = []
    if economy:
        gold = economy.get_gold()
        buy_buttons = draw_shop(left_panel, 0, 20, gold)

        # Ajuster les positions des boutons pour l'écran absolu
        for button in buy_buttons:
            button["rect"].x += current_left_x

    screen.blit(left_panel, (current_left_x, 0))

    # Onglet droit
    right_rect = pygame.Rect(current_right_x, 0, panel_width, screen_height)
    right_panel = pygame.Surface((panel_width, screen_height))
    right_panel.fill((50, 50, 50))
    screen.blit(right_panel, (current_right_x, 0))

    return left_rect, right_rect, current_left_x, current_right_x, buy_buttons
