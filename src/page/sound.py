import pygame
import os

SOUND_ASSETS_PATH = "src/assets/sounds/"


class Sound:
    """classe facilitant la gestion du son"""

    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self._preload_sounds()

    def _preload_sounds(self):
        """Précharge tous les sons"""
        if not os.path.exists(SOUND_ASSETS_PATH):
            return

        for filename in os.listdir(SOUND_ASSETS_PATH):
            if filename.endswith(('.wav', '.mp3')):
                sound_path = os.path.join(SOUND_ASSETS_PATH, filename)
                try:
                    self.sounds[filename] = pygame.mixer.Sound(sound_path)
                except pygame.error as e:
                    print(f"Erreur lors du chargement du son {filename}: {e}")

    def play(self, sound_file_name: str):
        """Joue le son passé en paramètre, seul le nom du fichier est nécessaire
        """
        if sound_file_name in self.sounds:
            self.sounds[sound_file_name].play()
        else:
            print(f"Avertissement: Le son '{sound_file_name}' n'a pas été trouvé")


# singleton a appeler pour jouer les sons (ne pas reinstancier le mixeur a chaque fois)
sound = Sound()
