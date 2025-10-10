import pygame

class SoundManager():
    """classe facilitant la gestion du son"""

    def __init__(self):
        pygame.mixer.init()

    def play_sound(self, sound_file_name: str):
        """Joue le son passé en paramètre, seul le nom du fichier est nécessaire"""
        sound = pygame.mixer.Sound("assets/sounds/" + sound_file_name)
        sound.play()