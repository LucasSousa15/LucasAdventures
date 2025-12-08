# game/entities/scenery.py (ajuste chão)
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
        
        # Offsets para movimento contínuo
        self.background_offset = 0
        self.ground_offset = 0
        
        # Cria nuvens
        self.init_clouds()
        
        print(f"✅ Cenário configurado: Chão em Y={GameConfig.GROUND_LEVEL}")
    
    def load_background(self):
        """Carrega o fundo"""
        path = GameConfig.asset_path("background", "background.jpg")
        self.background = self.asset_adapter.load_image(path, use_alpha=False)
        
        # Redimensiona para altura da tela
        bg_width, bg_height = self.background.get_size()
        scale = GameConfig.SCREEN_HEIGHT / bg_height
        self.bg_width = int(bg_width * scale)
        self.bg_height = int(bg_height * scale)
        self.background = pygame.transform.scale(self.background, (self.bg_width, self.bg_height))
        
        self.background_width = self.bg_width * 2
    
    def load_ground(self):
        """Carrega o chão - Ajustado para posição mais baixa"""
        path = GameConfig.asset_path("ground", "ground.png")
        self.ground_tile = self.asset_adapter.load_image(path)
        
        # Redimensiona para ter altura proporcional
        tile_width, tile_height = self.ground_tile.get_size()
        
        # Altura do chão = 15% da tela
        target_height = int(GameConfig.SCREEN_HEIGHT * 0.15)
        scale = target_height / tile_height
        
        self.ground_tile = pygame.transform.scale(
            self.ground_tile, 
            (int(tile_width * scale), target_height)
        )
        
        self.tile_width = self.ground_tile.get_width()
        self.tiles_needed = (GameConfig.SCREEN_WIDTH // self.tile_width) + 2
    
    def init_clouds(self):
        """Inicializa as nuvens menores"""
        self.clouds = []
        for _ in range(GameConfig.CLOUD_COUNT):
            cloud = Cloud(self.asset_adapter, GameConfig.SCREEN_WIDTH * 2)
            # Reduz tamanho das nuvens
            cloud.image = pygame.transform.scale(
                cloud.image,
                (int(cloud.image.get_width() * 0.3), 
                 int(cloud.image.get_height() * 0.3))
            )
            self.clouds.append(cloud)
    
    def update(self, game_speed):
        """Atualiza offsets para movimento"""
        # Move fundo
        self.background_offset -= GameConfig.BACKGROUND_SCROLL_SPEED * game_speed
        if self.background_offset <= -self.bg_width:
            self.background_offset = 0
        
        # Move chão
        self.ground_offset -= GameConfig.GROUND_SCROLL_SPEED * game_speed
        if self.ground_offset <= -self.tile_width:
            self.ground_offset = 0
        
        # Atualiza nuvens
        for cloud in self.clouds:
            cloud.update(self.background_offset)
    
    def draw_background(self, graphics_adapter):
        """Desenha fundo"""
        x1 = self.background_offset
        x2 = self.background_offset + self.bg_width
        
        graphics_adapter.draw_sprite(self.background, x1, 0)
        graphics_adapter.draw_sprite(self.background, x2, 0)
    
    def draw_ground(self, graphics_adapter):
        """Desenha chão"""
        ground_y = GameConfig.GROUND_LEVEL
        
        # Linha do horizonte (opcional, para referência)
        # pygame.draw.line(graphics_adapter.screen, (255, 0, 0), 
        #                 (0, ground_y), (GameConfig.SCREEN_WIDTH, ground_y), 1)
        
        for i in range(self.tiles_needed):
            x = i * self.tile_width + self.ground_offset
            graphics_adapter.draw_sprite(self.ground_tile, x, ground_y)
    
    def draw_clouds(self, graphics_adapter):
        """Desenha nuvens"""
        for cloud in self.clouds:
            cloud.draw(graphics_adapter, self.background_offset)
    
    def draw(self, graphics_adapter):
        """Desenha todas as camadas"""
        self.draw_background(graphics_adapter)
        self.draw_clouds(graphics_adapter)
        self.draw_ground(graphics_adapter)
        
        # DEBUG: Mostra linha do chão
        if hasattr(graphics_adapter, 'debug_mode') and graphics_adapter.debug_mode:
            pygame.draw.line(graphics_adapter.screen, (255, 0, 0),
                            (0, GameConfig.GROUND_LEVEL),
                            (GameConfig.SCREEN_WIDTH, GameConfig.GROUND_LEVEL), 2)