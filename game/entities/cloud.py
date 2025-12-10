
import pygame
import random
from game.utils.config import GameConfig

class Cloud:
    def __init__(self, asset_adapter, world_width):
        self.asset_adapter = asset_adapter
        self.world_width = world_width
        self.image = self.load_image()

        scale = random.uniform(0.15, 0.25)
        self.width = int(self.image.get_width() * scale)
        self.height = int(self.image.get_height() * scale)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.x = random.randint(0, world_width)
        self.y = random.randint(50, 250)

        self.speed = random.uniform(0.1, 0.3)
        self.opacity = random.randint(150, 220)
        self.image.set_alpha(self.opacity)

    def load_image(self):

        path = GameConfig.asset_path("cloud", "clean.png")
        return self.asset_adapter.load_image(path)

    def update(self, camera_offset_x):


        self.screen_x = self.x - camera_offset_x * self.speed

        if self.screen_x < -self.width:
            self.x += self.world_width + self.width + random.randint(100, 300)
            self.y = random.randint(50, 250)
            self.screen_x = self.x - camera_offset_x * self.speed
        elif self.screen_x > GameConfig.SCREEN_WIDTH:
            self.x -= self.world_width + self.width + random.randint(100, 300)
            self.y = random.randint(50, 250)
            self.screen_x = self.x - camera_offset_x * self.speed

    def draw(self, graphics_adapter, camera_offset_x):


        screen_x = self.x - camera_offset_x * self.speed
        screen_y = self.y

        if screen_x + self.width > -100 and screen_x < GameConfig.SCREEN_WIDTH + 100:
            graphics_adapter.draw_sprite(self.image, screen_x, screen_y)
