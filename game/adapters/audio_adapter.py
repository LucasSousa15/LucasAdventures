
import pygame
from abc import ABC, abstractmethod

class AudioAdapter(ABC):
    
    
    @abstractmethod
    def play_sound(self, sound_name, volume=1.0, loops=0):
        pass
    
    @abstractmethod
    def play_music(self, music_name, volume=1.0, loops=-1):
        pass
    
    @abstractmethod
    def stop_music(self):
        pass
    
    @abstractmethod
    def set_volume(self, volume):
        pass

class PygameAudioAdapter(AudioAdapter):
    
    
    def __init__(self, sounds_path="assets/sounds/"):
        pygame.mixer.init()
        self.sounds = {}
        self.current_music = None
        self.sounds_path = sounds_path
    
    def load_sound(self, name, file_path):
        
        try:
            self.sounds[name] = pygame.mixer.Sound(file_path)
            return True
        except Exception as e:
            print(f"Erro ao carregar som {name}: {e}")
            return False
    
    def play_sound(self, sound_name, volume=1.0, loops=0):
        
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            sound.set_volume(volume)
            sound.play(loops)
        else:

            file_path = f"{self.sounds_path}{sound_name}.wav"
            if self.load_sound(sound_name, file_path):
                self.play_sound(sound_name, volume, loops)
    
    def play_music(self, music_name, volume=1.0, loops=-1):
        
        try:
            pygame.mixer.music.load(f"{self.sounds_path}{music_name}.mp3")
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops)
            self.current_music = music_name
        except Exception as e:
            print(f"Erro ao carregar música {music_name}: {e}")
    
    def stop_music(self):
        
        pygame.mixer.music.stop()
        self.current_music = None
    
    def set_volume(self, volume):
        
        pygame.mixer.music.set_volume(volume)
        for sound in self.sounds.values():
            sound.set_volume(volume)