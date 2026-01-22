###############################
# COMPOSANTS UI RÉUTILISABLES #
###############################

from operator import pos
import pygame
from src.const import *

class Button:
    def __init__(self, text, x, y, action, color, color_hover, text_color):
        self.text = text
        self.action = action
        self.color = color
        self.color_hover = color_hover
        self.text_color = text_color
        self.width, self.height = BUTTON_WIDTH_LARGE, BUTTON_HEIGHT_LARGE
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

    def draw(self, win, mouse_pos, font):
        is_hover = self.rect.collidepoint(mouse_pos)
        color = self.color_hover if is_hover else self.color
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, color, (0, 0, self.width, self.height), border_radius=16)
        win.blit(button_surface, self.rect)

        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        shadow = font.render(self.text, True, SHADOW)
        
        win.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        win.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
## Toggle paramètres musique/sound
class Toggle:
    def __init__(self, label, center_x, center_y):
        self.label = label
        self.is_on = False
        size = (80, 70)
        
        # Charger les images
        try:
            img_on = pygame.image.load("src/assets/img/son_on.png").convert_alpha()
            self.img_on = pygame.transform.scale(img_on, size)
            img_off = pygame.image.load("src/assets/img/son_off.png").convert_alpha()
            self.img_off = pygame.transform.scale(img_off, size)
        except:
            self.img_on = None
            self.img_off = None
        
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.rect.center = (center_x, center_y)
        self.font = pygame.font.Font(None, 48)
    
    def draw(self, surface):
        # Label à gauche
        label_surf = self.font.render(self.label, True, TEXT_COLOR)
        label_rect = label_surf.get_rect(right=self.rect.left - 10, centery=self.rect.centery)
        surface.blit(label_surf, label_rect)
        
        # Image
        if self.img_on and self.img_off:
            img = self.img_on if self.is_on else self.img_off
            surface.blit(img, self.rect)
    
    def toggle(self):
        self.is_on = not self.is_on
        print(f"{self.label}: {'ON' if self.is_on else 'OFF'}")
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)