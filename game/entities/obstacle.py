
import pygame
import os
import random

from game.utils.config import GameConfig


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type: str, asset_adapter):
        super().__init__()

        

        self.type = obstacle_type
        self.asset_adapter = asset_adapter

        self.image = self.load_asset_or_placeholder()

        self.rect = self.image.get_rect()
        self.x = GameConfig.SCREEN_WIDTH + random.randint(50, 300)
        self.y = self.get_initial_y()

        self.rect.midbottom = (self.x, self.y)

        self.speed = GameConfig.OBSTACLE_SPEED



    def load_asset_or_placeholder(self):
        asset = self.try_load_asset()

        if asset:
            return asset

        if self.type == "cactus":
            width = GameConfig.CACTUS_WIDTH
            height = GameConfig.CACTUS_HEIGHT
            color = (0, 200, 0, 255)  # Verde forte (RGBA)
        else:  # bird
            width = GameConfig.BIRD_WIDTH
            height = GameConfig.BIRD_HEIGHT
            color = (200, 50, 50, 255)  # Vermelho (RGBA)

        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill(color)

        pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 4)

        return surface



    def try_load_asset(self):
        
        try:

            result = None
            try:
                result = self.asset_adapter.get_obstacle_asset(self.type, 0)
            except TypeError:


                try:
                    result = self.asset_adapter.get_obstacle_asset(self.type)
                except Exception:
                    result = None

            if result is None:
                return None

            if isinstance(result, pygame.Surface):
                image = result
            else:

                if isinstance(result, (str, bytes)) and os.path.exists(result):
                    image = pygame.image.load(result).convert_alpha()
                else:
                    return None

            if self.type == "cactus":
                size = (GameConfig.CACTUS_WIDTH, GameConfig.CACTUS_HEIGHT)
            else:  # bird
                size = (GameConfig.BIRD_WIDTH, GameConfig.BIRD_HEIGHT)

            return pygame.transform.scale(image, size)

        except Exception as e:
            print(f"[ERRO] Falha ao carregar asset de {self.type}: {e}")

        return None



    def get_initial_y(self):
        if self.type == "bird":

            return random.randint(GameConfig.BIRD_MIN_HEIGHT, GameConfig.BIRD_MAX_HEIGHT)
        else:

            return GameConfig.GROUND_LEVEL



    def update(self, delta_time):
        


        self.x -= self.speed * delta_time



        self.rect.midbottom = (int(self.x), int(self.y))

        if self.rect.right < 0:

            try:
                self.kill()
            except Exception:
                pass
            return True

        return False



    def draw(self, graphics_adapter):
        

        try:
            img_size = (self.image.get_width(), self.image.get_height())
        except Exception:
            img_size = None
        print(f"[DRAW] type={self.type} rect={self.rect} img_size={img_size}")

        if hasattr(graphics_adapter, "draw_sprite"):
            try:
                graphics_adapter.draw_sprite(self.image, int(self.rect.x), int(self.rect.y))
                return
            except Exception:
                pass

        if hasattr(graphics_adapter, "screen") and isinstance(graphics_adapter.screen, pygame.Surface):
            graphics_adapter.screen.blit(self.image, self.rect)
            return

        if isinstance(graphics_adapter, pygame.Surface):
            graphics_adapter.blit(self.image, self.rect)
            return

        raise AttributeError("graphics_adapter não possui draw_sprite nem screen.blit; passe o adapter correto.")
    