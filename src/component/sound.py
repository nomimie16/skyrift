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
        if sound_file_name not in self.sounds:
        if sound_file_name in self.sounds:
            self.sounds[sound_file_name].play(loops=loops)
        else:
            print(f"Le son '{sound_file_name}' n'a pas été trouvé")

    def play_loop(self, sound_file_name: str, identifier: str = None):
        """
        Joue un son en boucle infinie
        """
        if sound_file_name in self.sounds:
            self.sounds[sound_file_name].play()
        else:
            print(f"Avertissement: Le son '{sound_file_name}' n'a pas été trouvé")
            return

        if loop:
            # musique de fond
            if self.current_music == sound_file_name and pygame.mixer.music.get_busy():
                return  # déjà jouée, ne rien faire
            self.current_music = sound_file_name
            pygame.mixer.music.load(SOUND_ASSETS_PATH+sound_file_name)
            pygame.mixer.music.play(-1)  # boucle infinie
        else:
            # effet sonore
            self.sounds[sound_file_name].play()
            
    def stop_music(self):
        """Stop la musique de fond"""
        pygame.mixer.music.stop()
        self.current_music = None
            
    def stop_all(self):
        """Arrête tous les sons en cours de lecture"""
        pygame.mixer.stop()

    def stop(self, identifier: str):
        """
        Arrête un son en boucle
        """
        if identifier in self.looping_sounds:
            sound_file_name = self.looping_sounds[identifier]
            if sound_file_name in self.sounds:
                self.sounds[sound_file_name].stop()
            del self.looping_sounds[identifier]


# singleton a appeler pour jouer les sons (ne pas reinstancier le mixeur a chaque fois)
sound = Sound()
