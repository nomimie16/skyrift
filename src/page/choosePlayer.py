########################
# CHOIX DU MODE DE JEU #
########################
import pygame
from src.const import *
from src.page.ui_components import Button
from src.enum.game_mode import GameMode


def run_choose_player(screen):
    """Écran de sélection du mode de jeu"""
    
    # === RESSOURCES ===
    fond = pygame.image.load(IMG_BG_START).convert()
    fond = pygame.transform.scale(fond, (screen.get_width(), screen.get_height()))
    
    # Polices
    try:
        font_title = pygame.font.Font(FONT_TITLE_PATH, 80)
        font_subtitle = pygame.font.Font(FONT_BUTTON_PATH, 28)
        font_button = pygame.font.Font(FONT_BUTTON_PATH, 32)
    except:
        font_title = pygame.font.SysFont(None, 80)
        font_subtitle = pygame.font.SysFont(None, 28)
        font_button = pygame.font.SysFont(None, 32)
    
    # Dimensions
    width = screen.get_width()
    height = screen.get_height()
    center_x = width // 2
    center_y = height // 2
    
    # === MODE DE JEU SÉLECTIONNÉ ===
    selected_mode = None  # "pvp", "pvai", "aivai"
    
    # === BOUTONS DE MODE ===
    mode_buttons = [
        {
            "text": "Joueur vs Joueur",
            "mode": GameMode.PLAYER_VS_PLAYER.value,  # "pvp"
            "y": center_y - 120,
            "color": TRANSLUCENT_BLUE,
            "hover": HOVER_BLUE
        },
        {
            "text": "Joueur vs IA",
            "mode": GameMode.PLAYER_VS_AI.value,  # "pvai"
            "y": center_y,
            "color": TRANSLUCENT_BLUE,
            "hover": HOVER_BLUE
        },
        {
            "text": "IA vs IA",
            "mode": GameMode.AI_VS_AI.value,  # "aivai"
            "y": center_y + 120,
            "color": TRANSLUCENT_BLUE,
            "hover": HOVER_BLUE
        }
    ]
    
    # Créer les rectangles des boutons
    for btn in mode_buttons:
        btn["rect"] = pygame.Rect(0, 0, 400, 80)
        btn["rect"].center = (center_x, btn["y"])
    
    # === BOUTON COMMENCER ===
    btn_start_rect = pygame.Rect(0, 0, 300, 70)
    btn_start_rect.center = (center_x, height - 150)

    
    # === BOUCLE PRINCIPALE ===
    clock = pygame.time.Clock()
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ('quit', None)
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Vérifier les boutons de mode
                for btn in mode_buttons:
                    if btn["rect"].collidepoint(event.pos):
                        selected_mode = btn["mode"]
                        print(f"Mode sélectionné : {selected_mode}")
                
                # Bouton Commencer
                if btn_start_rect.collidepoint(event.pos) and selected_mode:
                    # Passer à l'écran de saisie des pseudos
                    result = show_pseudo_popup(screen, selected_mode, fond)
                    if result:
                        return result
                    

        # === AFFICHAGE ===
        screen.blit(fond, (0, 0))
        
        # Overlay semi-transparent
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))
        
        # Titre
        title = font_title.render("Choisissez votre mode", True, WHITE)
        title_shadow = font_title.render("Choisissez votre mode", True, SHADOW)
        title_x = center_x - title.get_width() // 2
        screen.blit(title_shadow, (title_x + 3, 83))
        screen.blit(title, (title_x, 80))
        
        # Sous-titre
        subtitle = font_subtitle.render("Sélectionnez un mode de jeu", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(center_x, 170))
        screen.blit(subtitle, subtitle_rect)
        
        # === BOUTONS DE MODE ===
        for btn in mode_buttons:
            is_hover = btn["rect"].collidepoint(mouse_pos)
            is_selected = (selected_mode == btn["mode"])
            
            # Couleur selon l'état
            if is_selected:
                color = HOVER_BLUE
                border_color = WHITE
                border_width = 4
            elif is_hover:
                color = btn["hover"]
                border_color = WHITE
                border_width = 2
            else:
                color = btn["color"]
                border_color = (200, 200, 200)
                border_width = 2
            
            # Fond du bouton
            button_surface = pygame.Surface((btn["rect"].width, btn["rect"].height), pygame.SRCALPHA)
            pygame.draw.rect(button_surface, color, (0, 0, btn["rect"].width, btn["rect"].height), border_radius=12)
            screen.blit(button_surface, btn["rect"])
            
            # Bordure
            pygame.draw.rect(screen, border_color, btn["rect"], border_width, border_radius=12)
            
            # Texte
            text_surf = font_button.render(btn["text"], True, WHITE)
            text_rect = text_surf.get_rect(center=btn["rect"].center)
            screen.blit(text_surf, text_rect)
        
        # === BOUTON COMMENCER ===
        can_start = selected_mode is not None
        start_color = HOVER_BROWN if can_start and btn_start_rect.collidepoint(mouse_pos) else TRANSLUCENT_BROWN if can_start else (100, 100, 100, 150)
        
        start_surface = pygame.Surface((btn_start_rect.width, btn_start_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(start_surface, start_color, (0, 0, btn_start_rect.width, btn_start_rect.height), border_radius=12)
        screen.blit(start_surface, btn_start_rect)
        
        start_text = font_button.render("Commencer !", True, WHITE if can_start else (150, 150, 150))
        start_text_rect = start_text.get_rect(center=btn_start_rect.center)
        screen.blit(start_text, start_text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return ('startGame', None)


def show_pseudo_popup(screen, mode, background):
    """Popup pour saisir les pseudos"""
    
    # Polices
    try:
        font_title = pygame.font.Font(FONT_BUTTON_PATH, 36)
        font_input = pygame.font.Font(FONT_BUTTON_PATH, 28)
    except:
        font_title = pygame.font.SysFont(None, 36)
        font_input = pygame.font.SysFont(None, 28)
    
    # Dimensions
    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2
    
    # Image de fond de la popup
    bg_pause = pygame.image.load(IMG_BG_PAUSE).convert_alpha()
    bg_pause = pygame.transform.scale(bg_pause, (500, 500))
    bg_rect = bg_pause.get_rect(center=(center_x, center_y))
    
    # Champs de saisie
    input_fields = []
    
    if mode == GameMode.PLAYER_VS_PLAYER.value:
        input_fields = [
            {"label": "Pseudo Joueur 1:", "value": "", "active": True},
            {"label": "Pseudo Joueur 2:", "value": "", "active": False}
        ]
    elif mode == GameMode.PLAYER_VS_AI.value:
        input_fields = [
            {"label": "Votre pseudo:", "value": "", "active": True}
        ]
    else:  # AI_VS_AI
        input_fields = []
    
    # Rectangles des champs
    input_y = center_y - 80
    for i, field in enumerate(input_fields):
        field["rect"] = pygame.Rect(center_x - 200, input_y + i * 100, 400, 50)
    
    # Boutons
    btn_validate = pygame.Rect(center_x - 100, center_y + 120, 200, 50)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ('quit', None)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Activer/désactiver les champs
                for field in input_fields:
                    field["active"] = field["rect"].collidepoint(event.pos)
                
                # Bouton valider
                if btn_validate.collidepoint(event.pos):
                    # Vérifier que tous les champs sont remplis
                    all_filled = all(field["value"].strip() != "" for field in input_fields)
                    
                    if mode == GameMode.AI_VS_AI.value or all_filled:
                        # Récupérer les pseudos
                        if mode == GameMode.PLAYER_VS_PLAYER.value:
                            p1_name = input_fields[0]["value"].strip()
                            p2_name = input_fields[1]["value"].strip()
                        elif mode == GameMode.PLAYER_VS_AI.value:
                            p1_name = input_fields[0]["value"].strip()
                            p2_name = "IA"
                        else:  # AI_VS_AI
                            p1_name = "IA 1"
                            p2_name = "IA 2"
                        
                        return ('game', {'mode': mode, 'p1': p1_name, 'p2': p2_name})
            
            if event.type == pygame.KEYDOWN:
                for field in input_fields:
                    if field["active"]:
                        if event.key == pygame.K_RETURN:
                            # Passer au champ suivant ou valider
                            idx = input_fields.index(field)
                            if idx < len(input_fields) - 1:
                                field["active"] = False
                                input_fields[idx + 1]["active"] = True
                            else:
                                # Simuler clic sur valider
                                all_filled = all(f["value"].strip() != "" for f in input_fields)
                                if mode == GameMode.AI_VS_AI.value or all_filled:
                                    # Récupérer les pseudos
                                    if mode == GameMode.PLAYER_VS_PLAYER.value:
                                        p1_name = input_fields[0]["value"].strip()
                                        p2_name = input_fields[1]["value"].strip()
                                    elif mode == GameMode.PLAYER_VS_AI.value:
                                        p1_name = input_fields[0]["value"].strip()
                                        p2_name = "IA"
                                    else:  # AI_VS_AI
                                        p1_name = "IA 1"
                                        p2_name = "IA 2"
                                    
                                    return ('game', {'mode': mode, 'p1': p1_name, 'p2': p2_name})
                        
                        elif event.key == pygame.K_BACKSPACE:
                            field["value"] = field["value"][:-1]
                        elif event.key == pygame.K_ESCAPE:
                            return None
                        else:
                            if len(field["value"]) < 15:
                                field["value"] += event.unicode
        
        # === AFFICHAGE ===
        screen.blit(background, (0, 0))
        
        # Overlay semi-transparent
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(OVERLAY_ALPHA)
        overlay.fill(OVERLAY_COLOR)
        screen.blit(overlay, (0, 0))
        
        # Image de fond de la popup
        screen.blit(bg_pause, bg_rect)
        
        # Titre
        if mode == GameMode.AI_VS_AI.value:
            title_text = "Mode IA vs IA"
        else:
            title_text = "Entrez vos pseudos"
       
        title = font_title.render(title_text, True, BROWN_FONT)
        title_rect = title.get_rect(center=(center_x, bg_rect.top + 60))
        screen.blit(title, title_rect)
        
        # Champs de saisie
        for field in input_fields:
            # Fond
            field_color = (255, 250, 240) if field["active"] else (245, 240, 230)
            pygame.draw.rect(screen, field_color, field["rect"], border_radius=8)
            pygame.draw.rect(screen, BROWN_FONT if field["active"] else (150, 120, 90), field["rect"], 2, border_radius=8)
            
            # Label
            label = font_input.render(field["label"], True, BROWN_FONT)
            label_rect = label.get_rect(bottomleft=(field["rect"].left, field["rect"].top - 5))
            screen.blit(label, label_rect)
            
            # Texte saisi
            text = font_input.render(field["value"] + ("|" if field["active"] else ""), True, TRANSLUCENT_BROWN)
            text_rect = text.get_rect(left=field["rect"].left + 10, centery=field["rect"].centery)
            screen.blit(text, text_rect)
        
        # Bouton Valider
        all_filled = all(f["value"].strip() != "" for f in input_fields) or mode == GameMode.AI_VS_AI.value
        mouse_pos = pygame.mouse.get_pos()
        is_hover = btn_validate.collidepoint(mouse_pos) and all_filled
        
        btn_color = HOVER_BROWN if is_hover else TRANSLUCENT_BROWN if all_filled else (150, 150, 150, 150)
        
        # Fond du bouton avec transparence
        btn_surface = pygame.Surface((btn_validate.width, btn_validate.height), pygame.SRCALPHA)
        pygame.draw.rect(btn_surface, btn_color, (0, 0, btn_validate.width, btn_validate.height), border_radius=12)
        screen.blit(btn_surface, btn_validate)
        
        validate_text = font_title.render("Valider", True, BROWN_FONT if all_filled else (100, 100, 100))
        validate_rect = validate_text.get_rect(center=btn_validate.center)
        screen.blit(validate_text, validate_rect)
        
        # Message si IA vs IA
        if mode == GameMode.AI_VS_AI.value:
            msg = font_input.render("Appuyez sur Valider pour lancer", True, BROWN_FONT)
            msg_rect = msg.get_rect(center=(center_x, center_y + 20))
            screen.blit(msg, msg_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return None