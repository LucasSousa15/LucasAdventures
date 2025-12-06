import pygame
import random
from game.utils.config import GameConfig
from game.entities.cloud import Cloud

class Scenery:
    def __init__(self, asset_adapter):
        self.asset_adapter = asset_adapter
        self.load_background()
        self.load_ground()
        self.clouds = []
        self.background_offset = 0
        
        # Cria nuvens
        for _ in range(GameConfig.CLOUD_COUNT):
            self.clouds.append(Cloud(asset_adapter))
    
    def load_background(self):
        """Carrega o fundo e redimensiona para a tela"""
        path = GameConfig.asset_path("background", "background.jpg")
        self.background = self.asset_adapter.load_image(path, use_alpha=False)
        
        # Redimensiona para cobrir a tela (mantendo proporção)
        bg_width, bg_height = self.background.get_size()
        scale = max(GameConfig.SCREEN_WIDTH / bg_width, 
                   GameConfig.SCREEN_HEIGHT / bg_height)
        
        new_width = int(bg_width * scale)
        new_height = int(bg_height * scale)
        self.background = pygame.transform.scale(self.background, (new_width, new_height))
        
        # Para efeito de rolagem contínua, criamos uma imagem mais larga
        self.background_width = new_width * 2
        self.scrolling_background = pygame.Surface((self.background_width, new_height))
        
        # Preenche a superfície com duas cópias do fundo lado a lado
        for i in range(2):
            self.scrolling_background.blit(self.background, (i * new_width, 0))
    
    def load_ground(self):
        """Carrega o chão e prepara para repetição"""
        path = GameConfig.asset_path("ground", "ground.png")
        self.ground_tile = self.asset_adapter.load_image(path)
        
        # Redimensiona o chão para ter altura apropriada
        tile_width, tile_height = self.ground_tile.get_size()
        ground_scale = 0.3  # Ajuste conforme necessário
        new_ground_height = int(GameConfig.SCREEN_HEIGHT * 0.15)  # 15% da tela
        ground_scale = new_ground_height / tile_height
        
        self.ground_tile = pygame.transform.scale(
            self.ground_tile, 
            (int(tile_width * ground_scale), int(tile_height * ground_scale))
        )
        
        # Calcula quantas vezes repetir o chão
        self.tile_width = self.ground_tile.get_width()
        self.tiles_needed = (GameConfig.SCREEN_WIDTH // self.tile_width) + 2
    
    def update(self, player_dx):
        """Atualiza o cenário baseado no movimento do jogador"""
        # Atualiza posição do fundo (parallax)
        self.background_offset -= player_dx * GameConfig.BACKGROUND_SCROLL_SPEED
        
        # Mantém o offset dentro dos limites
        if abs(self.background_offset) >= self.background.get_width():
            self.background_offset = 0
        
        # Atualiza nuvens
        for cloud in self.clouds:
            cloud.update(player_dx)
    
    def draw_background(self, graphics_adapter):
        """Desenha o fundo com rolagem"""
        # Calcula a posição de desenho
        draw_x = self.background_offset % self.background.get_width()
        
        # Desenha duas cópias para rolagem contínua
        graphics_adapter.draw_sprite(self.background, draw_x, 0)
        graphics_adapter.draw_sprite(self.background, 
                                   draw_x - self.background.get_width(), 
                                   0)
    
    def draw_ground(self, graphics_adapter):
        """Desenha o chão repetido"""
        ground_y = GameConfig.GROUND_LEVEL
        
        for i in range(self.tiles_needed):
            x = (i * self.tile_width) - (self.background_offset * 0.1) % self.tile_width
            graphics_adapter.draw_sprite(self.ground_tile, x, ground_y)
    
    def draw_clouds(self, graphics_adapter):
        """Desenha todas as nuvens"""
        for cloud in self.clouds:
            cloud.draw(graphics_adapter)
    
    def draw(self, graphics_adapter):
        """Desenha todas as camadas do cenário"""
        # 1. Fundo
        self.draw_background(graphics_adapter)
        
        # 2. Nuvens
        self.draw_clouds(graphics_adapter)
        
        # 3. Chão
        self.draw_ground(graphics_adapter)