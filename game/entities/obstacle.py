
import pygame
import os
import random

from game.utils.config import GameConfig


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type: str, asset_adapter, size: tuple = None):
        super().__init__()




        self.override_size = size

        self.type = obstacle_type
        self.asset_adapter = asset_adapter

        self.image = self.load_asset_or_placeholder()

        self.rect = self.image.get_rect()
        self.x = GameConfig.SCREEN_WIDTH + random.randint(50, 300)
        self.y = self.get_initial_y()

        self.rect.midbottom = (self.x, self.y)


        self.speed = GameConfig.OBSTACLE_SPEED



        if self.type == "cactus":
            cw = int(self.rect.width * 0.75)
            ch = int(self.rect.height * 0.9)
        else:
            cw = int(self.rect.width * 0.6)
            ch = int(self.rect.height * 0.6)

        self.collision_rect = pygame.Rect(0, 0, max(1, cw), max(1, ch))

        self.collision_rect.midbottom = self.rect.midbottom



    def load_asset_or_placeholder(self):
        asset = self.try_load_asset()

        if asset:
            return asset

        if self.type == "cactus":
            if self.override_size:
                width, height = self.override_size
            else:
                width = GameConfig.CACTUS_WIDTH
                height = GameConfig.CACTUS_HEIGHT
            color = (0, 200, 0, 255)
        else:
            if self.override_size:
                width, height = self.override_size
            else:
                width = GameConfig.BIRD_WIDTH
                height = GameConfig.BIRD_HEIGHT
            color = (200, 50, 50, 255)

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

            if self.override_size:
                size = tuple(self.override_size)
            else:
                if self.type == "cactus":
                    size = (GameConfig.CACTUS_WIDTH, GameConfig.CACTUS_HEIGHT)
                else:
                    size = (GameConfig.BIRD_WIDTH, GameConfig.BIRD_HEIGHT)

            return pygame.transform.scale(image, size)

        except Exception:
            pass

        return None



    def get_initial_y(self):
        if self.type == "bird":


            safe_min_height = max(
                GameConfig.BIRD_MIN_HEIGHT,
                GameConfig.GROUND_LEVEL - (GameConfig.PLAYER_HEIGHT * 0.9)
            )
            safe_max_height = GameConfig.BIRD_MAX_HEIGHT
            return random.randint(safe_min_height, safe_max_height)
        else:
            return GameConfig.GROUND_LEVEL



    def update(self, delta_time):



        self.x -= self.speed * delta_time



        self.rect.midbottom = (int(self.x), int(self.y))

        try:
            self.collision_rect.midbottom = self.rect.midbottom
        except Exception:
            pass

        if self.rect.right < 0:

            try:
                self.kill()
            except Exception:
                pass
            return True

        return False



    def draw(self, graphics_adapter):



        drew = False

        if hasattr(graphics_adapter, "draw_sprite"):
            try:
                graphics_adapter.draw_sprite(self.image, int(self.rect.x), int(self.rect.y))
                drew = True
            except Exception:
                drew = False


        if not drew:
            if hasattr(graphics_adapter, "screen") and isinstance(graphics_adapter.screen, pygame.Surface):
                graphics_adapter.screen.blit(self.image, self.rect)
                drew = True
            elif isinstance(graphics_adapter, pygame.Surface):
                graphics_adapter.blit(self.image, self.rect)
                drew = True

        if not drew:
            raise AttributeError("graphics_adapter não possui draw_sprite nem screen.blit; passe o adapter correto.")


        try:
            if getattr(GameConfig, "DEBUG_SHOW_COLLISIONS", False):

                if hasattr(graphics_adapter, "draw_rect"):
                    graphics_adapter.draw_rect((255, 0, 0), self.collision_rect, 2)
                elif hasattr(graphics_adapter, "screen") and isinstance(graphics_adapter.screen, pygame.Surface):
                    pygame.draw.rect(graphics_adapter.screen, (255, 0, 0), self.collision_rect, 2)
        except Exception:
            pass



        try:
            bound = self.image.get_bounding_rect()
            if bound.width == 0 or bound.height == 0:

                placeholder = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                placeholder.fill((200, 0, 0, 180))
                if hasattr(graphics_adapter, "screen") and isinstance(graphics_adapter.screen, pygame.Surface):
                    graphics_adapter.screen.blit(placeholder, self.rect)

                    try:
                        font = pygame.font.Font(None, 20)
                        txt = font.render("OBST", True, (255, 255, 255))
                        graphics_adapter.screen.blit(txt, (self.rect.x + 4, self.rect.y + 4))
                    except Exception:
                        pass
                else:

                    try:
                        graphics_adapter.draw_sprite(placeholder, int(self.rect.x), int(self.rect.y))
                    except Exception:
                        pass
        except Exception:
            pass

    def get_collision_rect(self):
        """Return the current collision rect (keeps it in sync with visual rect)."""
        return self.collision_rect



