
import pygame
import os
from abc import ABC, abstractmethod

class AssetAdapter(ABC):
    
    
    @abstractmethod
    def load_image(self, path, use_alpha=True):
        pass
    
    @abstractmethod
    def load_animation_frames(self, folder, animation_name, frame_count):
        pass

class PygameAssetAdapter(AssetAdapter):
    
    
    def load_image(self, path, use_alpha=True):
        try:
            if use_alpha:
                return pygame.image.load(path).convert_alpha()
            return pygame.image.load(path).convert()
        except Exception as e:
            print(f"Erro ao carregar imagem {path}: {e}")
            return self._create_fallback_surface()
    
    def load_animation_frames(self, folder, animation_name, frame_count):
        frames = []
        for i in range(frame_count):
            frame_path = os.path.join(folder, f"{animation_name}_{i}.png")
            frames.append(self.load_image(frame_path))
        return frames
    
    def _create_fallback_surface(self):
        
        surf = pygame.Surface((64, 64))
        surf.fill((255, 0, 255))  # Magenta para destacar
        return surf