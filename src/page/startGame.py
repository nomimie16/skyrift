########################
# FENETRE DEBUT DU JEU #
########################

import pygame

from src.sound import Sound


def run_start(screen):
    sound = Sound()
    # ===== RESSOURCES =====

    # Taille de l'écran
    WIDTH = screen.get_width()

    # Couleurs
    WHITE = (255, 255, 255)
    TRANSLUCENT_BLUE = (0, 120, 200, 180)
    HOVER_BLUE = (0, 140, 255, 220)
    SHADOW = (0, 0, 0)

    # Images
    fond = pygame.image.load('src/assets/img/bgStart.png')
    fond = fond.convert()

    # Polices
    try:
        FONT_TITLE = pygame.font.Font("src/assets/font/test1.ttf", 100)
        FONT_BUTTON = pygame.font.Font("src/assets/font/BoldPixels.ttf", 36)
    except:
        FONT_TITLE = pygame.font.SysFont(None, 100)
        FONT_BUTTON = pygame.font.SysFont(None, 36)

    # Musique
    # mixer.music.load('assets/sound/startMusic.mp3')
    # mixer.music.play(-1)

    # ===== FIN RESSOURCES =====

    # ==== CLASSE BOUTONS ======
    class Button:
        def __init__(self, text, center_y, action):
            self.text = text
            self.action = action
            self.center_y = center_y
            self.width, self.height = 320, 70
            self.rect = pygame.Rect((0, 0, self.width, self.height))
            self.rect.center = (WIDTH // 2, center_y)

        def draw(self, win, mouse_pos):
            is_hover = self.rect.collidepoint(mouse_pos)
            color = HOVER_BLUE if is_hover else TRANSLUCENT_BLUE
            button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(button_surface, color, (0, 0, self.width, self.height), border_radius=16)
            win.blit(button_surface, self.rect)

            text_surf = FONT_BUTTON.render(self.text, True, WHITE)
            text_rect = text_surf.get_rect(center=self.rect.center)

            shadow = FONT_BUTTON.render(self.text, True, SHADOW)
            win.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
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
                        sound.play("temp.mp3")
                        print(f"Action : {button.action}")
                        return button.action

        screen.fill((0, 0, 0))

        screen.blit(fond, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Titre
        title = FONT_TITLE.render("SkyRift", True, WHITE)
        shadow = FONT_TITLE.render("SkyRift", True, SHADOW)
        screen.blit(shadow, (WIDTH // 2 - title.get_width() // 2 + 3, 103))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        for button in buttons:
            button.draw(screen, mouse_pos)

        pygame.display.flip()

    return None
