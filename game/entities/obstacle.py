
import pygame
import os
import random

from game.utils.config import GameConfig


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type: str, asset_adapter, size: tuple = None):
        super().__init__()

        # optional override size: (width, height). If provided, obstacle will use
        # this size instead of the static values in GameConfig. This allows
        # dynamic sizing based on the player's current size.
        self.override_size = size

        self.type = obstacle_type
        self.asset_adapter = asset_adapter

        self.image = self.load_asset_or_placeholder()

        self.rect = self.image.get_rect()
        self.x = GameConfig.SCREEN_WIDTH + random.randint(50, 300)
        self.y = self.get_initial_y()

        self.rect.midbottom = (self.x, self.y)

        # Logical movement speed (will be adjusted by GameManager)
        self.speed = GameConfig.OBSTACLE_SPEED

        # Create a tighter collision/hitbox so obstacles are not "ghosts".
        # We keep the visual `rect` for drawing, but use `collision_rect` for collisions.
        if self.type == "cactus":
            cw = int(self.rect.width * 0.75)
            ch = int(self.rect.height * 0.9)
        else:  # bird
            cw = int(self.rect.width * 0.6)
            ch = int(self.rect.height * 0.6)

        self.collision_rect = pygame.Rect(0, 0, max(1, cw), max(1, ch))
        # align collision box to the sprite's bottom center
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
            color = (0, 200, 0, 255)  # Verde forte (RGBA)
        else:  # bird
            if self.override_size:
                width, height = self.override_size
            else:
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

            if self.override_size:
                size = tuple(self.override_size)
            else:
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
        # keep collision rect aligned with visual rect
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
        

        # Draw the visual sprite (collision handled separately)
        drew = False
        # try adapter draw_sprite first
        if hasattr(graphics_adapter, "draw_sprite"):
            try:
                graphics_adapter.draw_sprite(self.image, int(self.rect.x), int(self.rect.y))
                drew = True
            except Exception:
                drew = False

        # fallback to direct blit
        if not drew:
            if hasattr(graphics_adapter, "screen") and isinstance(graphics_adapter.screen, pygame.Surface):
                graphics_adapter.screen.blit(self.image, self.rect)
                drew = True
            elif isinstance(graphics_adapter, pygame.Surface):
                graphics_adapter.blit(self.image, self.rect)
                drew = True

        if not drew:
            raise AttributeError("graphics_adapter não possui draw_sprite nem screen.blit; passe o adapter correto.")

        # Draw collision rectangle for debugging if enabled
        try:
            if getattr(GameConfig, "DEBUG_SHOW_COLLISIONS", False):
                # prefer adapter draw_rect if available
                if hasattr(graphics_adapter, "draw_rect"):
                    graphics_adapter.draw_rect((255, 0, 0), self.collision_rect, 2)
                elif hasattr(graphics_adapter, "screen") and isinstance(graphics_adapter.screen, pygame.Surface):
                    pygame.draw.rect(graphics_adapter.screen, (255, 0, 0), self.collision_rect, 2)
        except Exception:
            pass

        # If the sprite appears fully transparent (no opaque pixels), draw a visible fallback
        # so the player can see and avoid the obstacle.
        try:
            bound = self.image.get_bounding_rect()
            if bound.width == 0 or bound.height == 0:
                # draw a semi-opaque placeholder rectangle at the visual rect
                placeholder = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                placeholder.fill((200, 0, 0, 180))
                if hasattr(graphics_adapter, "screen") and isinstance(graphics_adapter.screen, pygame.Surface):
                    graphics_adapter.screen.blit(placeholder, self.rect)
                    # label
                    try:
                        font = pygame.font.Font(None, 20)
                        txt = font.render("OBST", True, (255, 255, 255))
                        graphics_adapter.screen.blit(txt, (self.rect.x + 4, self.rect.y + 4))
                    except Exception:
                        pass
                else:
                    # fallback to adapter draw_sprite with placeholder
                    try:
                        graphics_adapter.draw_sprite(placeholder, int(self.rect.x), int(self.rect.y))
                    except Exception:
                        pass
        except Exception:
            pass

    def get_collision_rect(self):
        """Return the current collision rect (keeps it in sync with visual rect)."""
        return self.collision_rect

        
    