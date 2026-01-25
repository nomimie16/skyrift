import pygame

from src.const import FONT_BUTTON_PATH


class GoldPopup:
    """Classe pour afficher les popups de gain/perte d'or."""

    def __init__(self, x, y, amount, duration=1000):
        self.x = x
        self.y = y
        self.start_y = y
        self.start_time = pygame.time.get_ticks()
        self.amount = amount
        self.duration = duration

        self.font = pygame.font.Font(FONT_BUTTON_PATH, 45)

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

    def draw(self, screen, offset_x=0) -> None:
        """
        Dessine le texte flottant à l'écran
        :param offset_x: décéntage en x
        :param screen:
        :return:
        """
        text_surf = self.font.render(self.text, True, self.color)
        rect = text_surf.get_rect(center=(self.x + offset_x, self.y))
        screen.blit(text_surf, rect)


class GoldPopupManager:
    """Gestionnaire pour les popups de gain/perte d'or."""

    def __init__(self):
        self.popups = []

    def spawn(self, x, y, amount):
        """
        Crée un texte flottant pour une position donnée
        :param x:
        :param y:
        :param amount:
        :return:
        """
        self.popups.append(GoldPopup(x, y, amount))

    def update_and_draw(self, screen, offset_x=0):
        """
        Met à jour et dessine tous les textes flottants
        :param offset_x: décéntage en x
        :param screen:
        :return:
        """
        for text in self.popups[:]:
            text.update()
            text.draw(screen, offset_x)
            if not text.alive:
                self.popups.remove(text)
