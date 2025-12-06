
import pygame
from game.utils.config import GameConfig

class Camera:
    def __init__(self):
        self.width = GameConfig.SCREEN_WIDTH
        self.height = GameConfig.SCREEN_HEIGHT
        self.world_width = GameConfig.LEVEL_WIDTH
        self.camera = pygame.Rect(0, 0, self.width, self.height)
    
    def update(self, target):
        

        target_x = target.rect.centerx

        camera_x = target_x - self.width // 2

        camera_x = max(0, camera_x)  # Não pode ir além do início (esquerda)
        camera_x = min(camera_x, self.world_width - self.width)  # Não pode ir além do fim (direita)

        self.camera.x = camera_x
    
    def apply(self, entity_rect):
        
        return entity_rect.move(-self.camera.x, 0)
    
    def apply_to_pos(self, x, y):
        
        return x - self.camera.x, y
    
    def get_offset_x(self):
        
        return self.camera.x