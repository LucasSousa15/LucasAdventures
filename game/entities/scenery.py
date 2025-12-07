
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

        self.init_clouds()
    
    def load_background(self):
        
        path = GameConfig.asset_path("background", "background.jpg")
        self.background = self.asset_adapter.load_image(path, use_alpha=False)

        bg_width, bg_height = self.background.get_size()
        scale = GameConfig.SCREEN_HEIGHT / bg_height
        self.bg_width = int(bg_width * scale)
        self.bg_height = int(bg_height * scale)
        self.background = pygame.transform.scale(self.background, (self.bg_width, self.bg_height))

        self.bg_copies = max(3, (GameConfig.LEVEL_WIDTH // self.bg_width) + 2)
    
    def load_ground(self):
        
        path = GameConfig.asset_path("ground", "ground.png")
        self.ground_tile = self.asset_adapter.load_image(path)

        tile_width, tile_height = self.ground_tile.get_size()
        ground_scale = GameConfig.SCREEN_HEIGHT * 0.15 / tile_height  # 15% da tela
        
        self.ground_tile = pygame.transform.scale(
            self.ground_tile, 
            (int(tile_width * ground_scale), int(tile_height * ground_scale))
        )
        
        self.tile_width = self.ground_tile.get_width()
        self.ground_copies = (GameConfig.LEVEL_WIDTH // self.tile_width) + 2
    
    def init_clouds(self):
        
        self.clouds = []
        for _ in range(GameConfig.CLOUD_COUNT):
            cloud = Cloud(self.asset_adapter, GameConfig.LEVEL_WIDTH)
            self.clouds.append(cloud)
    
    def update(self, camera_offset_x):
        

        for cloud in self.clouds:
            cloud.update(camera_offset_x)
    
    def draw_background(self, graphics_adapter, camera_offset_x):
        

        start_tile = int(camera_offset_x / self.bg_width)

        for i in range(start_tile - 1, start_tile + 3):
            x = i * self.bg_width - camera_offset_x
            graphics_adapter.draw_sprite(self.background, x, 0)
    
    def draw_ground(self, graphics_adapter, camera_offset_x):
        
        ground_y = GameConfig.GROUND_LEVEL

        start_tile = int(camera_offset_x / self.tile_width)

        for i in range(start_tile - 1, start_tile + 4):
            x = i * self.tile_width - camera_offset_x
            if x + self.tile_width > 0 and x < GameConfig.SCREEN_WIDTH:
                graphics_adapter.draw_sprite(self.ground_tile, x, ground_y)
    
    def draw_clouds(self, graphics_adapter, camera_offset_x):
        
        for cloud in self.clouds:
            cloud.draw(graphics_adapter, camera_offset_x)
    
    def draw(self, graphics_adapter, camera_offset_x):
        

        bg_offset_x = camera_offset_x * GameConfig.BACKGROUND_SCROLL_SPEED
        self.draw_background(graphics_adapter, bg_offset_x)

        self.draw_clouds(graphics_adapter, camera_offset_x)

        self.draw_ground(graphics_adapter, camera_offset_x)