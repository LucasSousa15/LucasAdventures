
import pygame
from abc import ABC, abstractmethod

class AudioAdapter(ABC):


    @abstractmethod
    def play_sound(self, sound_name, volume=1.0, loops=0):
        pass

    @abstractmethod
    def play_music(self, music_name, volume=1.0, loops=-1):
        pass

class PygameAudioAdapter(AudioAdapter):


    def __init__(self):
        try:
            pygame.mixer.init()
            self.sounds = {}
            print("✓ Sistema de áudio inicializado")
        except Exception as e:
            print(f"✗ Erro ao inicializar áudio: {e}")
            self.sounds = None

    def load_sound(self, path, name):

        if self.sounds is None:
            return False

        try:
            self.sounds[name] = pygame.mixer.Sound(path)
            return True
        except Exception as e:
            print(f"Erro ao carregar som {name}: {e}")
            return False

    def play_sound(self, sound_name, volume=1.0, loops=0):

        if self.sounds is None or sound_name not in self.sounds:
            return

        try:
            sound = self.sounds[sound_name]
            sound.set_volume(volume)
            sound.play(loops)
        except Exception as e:
            print(f"Erro ao tocar som {sound_name}: {e}")

    def play_music(self, music_name, volume=1.0, loops=-1):

        if pygame.mixer.get_init():
            try:
                pygame.mixer.music.set_volume(volume)
                print(f"Música {music_name} tocando (placeholder)")



            except Exception as e:
                print(f"Erro ao tocar música: {e}")
