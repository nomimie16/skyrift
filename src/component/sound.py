import pygame
import os

SOUND_ASSETS_PATH = "src/assets/sounds/"


class Sound:
    """classe facilitant la gestion du son"""

    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.looping_sounds = {}
        self._preload_sounds()
        self.current_music = None

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

    def play(self, sound_file_name: str, loops: int = 0):
        """Joue le son passé en paramètre, seul le nom du fichier est nécessaire
        """
        if sound_file_name in self.sounds:
            self.sounds[sound_file_name].play()
            self.sounds[sound_file_name].play(loops=loops)
        else:
            print(f"Le son '{sound_file_name}' n'a pas été trouvé")

    def play_loop(self, sound_file_name: str, identifier: str = None):
        """
        Joue un son en boucle infinie
        """
        if sound_file_name in self.sounds:
            if identifier and identifier in self.looping_sounds:
                self.stop(identifier)

            self.sounds[sound_file_name].play(loops=-1)
            if identifier:
                self.looping_sounds[identifier] = sound_file_name
        else:
            print(f"Avertissement: Le son '{sound_file_name}' n'a pas été trouvé")
            
    def stop(self, identifier: str):
        """
        Arrête un son en boucle
        """
        if identifier in self.looping_sounds:
            sound_file_name = self.looping_sounds[identifier]
            if sound_file_name in self.sounds:
                self.sounds[sound_file_name].stop()
            del self.looping_sounds[identifier]
            
    def stop_all(self):
        """Arrête tous les sons en cours de lecture"""
        pygame.mixer.stop()


# singleton a appeler pour jouer les sons (ne pas reinstancier le mixeur a chaque fois)
sound = Sound()
