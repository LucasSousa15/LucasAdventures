import pygame
import random
from game.utils.config import GameConfig

class Cloud:
    def __init__(self, asset_adapter):
        self.asset_adapter = asset_adapter
        self.image = self.load_image()
        
        # Tamanho aleatório para variedade
        scale = random.uniform(0.5, 1.2)
        self.width = int(self.image.get_width() * scale)
        self.height = int(self.image.get_height() * scale)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        # Posição inicial aleatória
        self.x = random.randint(0, GameConfig.SCREEN_WIDTH)
        self.y = random.randint(50, 400)  # Nuvens no topo da tela
        
        # Velocidade aleatória (nuvens maiores mais devagar para efeito parallax)
        self.speed = GameConfig.CLOUD_SPEED * random.uniform(0.3, 0.8) / scale
        self.opacity = random.randint(180, 255)
        
        # Cria uma cópia da imagem com opacidade
        self.image.set_alpha(self.opacity)
    
    def load_image(self):
        """Carrega a imagem da nuvem"""
        path = GameConfig.asset_path("cloud", "clean.png")
        return self.asset_adapter.load_image(path)
    
    def update(self, player_dx):
        """Atualiza posição baseada no movimento do jogador"""
        # Nuvens se movem na direção oposta ao jogador (parallax)
        self.x -= player_dx * self.speed * 0.3
        
        # Reseta posição se sair da tela
        if self.x < -self.width:
            self.x = GameConfig.SCREEN_WIDTH
            self.y = random.randint(50, 400)
        elif self.x > GameConfig.SCREEN_WIDTH:
            self.x = -self.width
            self.y = random.randint(50, 400)
    
    def draw(self, graphics_adapter):
        """Desenha a nuvem"""
        graphics_adapter.draw_sprite(self.image, self.x, self.y)