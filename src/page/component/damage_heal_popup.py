import pygame
from src.const import FONT_BUTTON_PATH

class DamageAndHealPopup:
    """Classe représentant un texte flottant pour les dégâts ou soins reçus par une entité"""

    def __init__(self, x, y, amount, duration=800):
        self.amount = amount
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        self.x = x
        self.y = y
        self.start_y = y

        self.font = pygame.font.Font(FONT_BUTTON_PATH, 24)

        if amount > 0:
            self.color = (50, 200, 50)  # Heal (vert)
            self.text = f"+{amount}"
        else:
            self.color = (220, 50, 50)  # Damage (rouge)
            self.text = f"{amount}"

        self.alive = True

    def update(self) -> None:
        """Met à jour la position et l'état du texte flottant"""
        elapsed = pygame.time.get_ticks() - self.start_time
        self.y = self.start_y - elapsed * 0.03

        if elapsed > self.duration:
            self.alive = False

    def draw(self, screen):
        """
        Dessine le texte flottant à l'écran
        :param screen:
        :return:
        """
        text_surf = self.font.render(self.text, True, self.color)
        rect = text_surf.get_rect(center=(self.x, self.y))
        screen.blit(text_surf, rect)


class DamageAndHealPopupManager:
    """Gestionnaire pour les textes flottants de dégâts et soins"""

    def __init__(self):
        self.popups = []

    def spawn_for_entity(self, entity, amount):
        """
        Crée un texte flottant pour une entité donnée
        :param entity:  Entité cible
        :param amount: Montant des dégâts ou soins
        :return:
        """
        x = entity.pixel_pos.x + 32
        y = entity.pixel_pos.y - 10
        self.popups.append(DamageAndHealPopup(x, y, amount))

    def update_and_draw(self, screen):
        """
        Met à jour et dessine tous les textes flottants
        :param screen:
        :return:
        """
        for text in self.popups[:]:
            text.update()
            text.draw(screen)
            if not text.alive:
                self.popups.remove(text)
