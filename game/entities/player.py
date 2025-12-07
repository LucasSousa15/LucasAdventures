
import pygame
from game.adapters.asset_adapter import PygameAssetAdapter
from game.utils.config import GameConfig

class Player:
    def __init__(self, x, y, asset_adapter=None):
        self.asset_adapter = asset_adapter or PygameAssetAdapter()
        self.load_animations()
        
        self.ground_y = y
        self.action = "idle"
        self.image = self.animations["idle"][0]
        self.frame_idx = 0.0
        self.flip = False

        self.vy = 0
        self.on_ground = True

        self.last_dx = 0

        if self.animations["idle"]:
            frame_width = self.animations["idle"][0].get_width()
            frame_height = self.animations["idle"][0].get_height()
        else:
            frame_width, frame_height = 120, 160
            
        self.rect = pygame.Rect(0, 0, frame_width * 0.6, frame_height * 0.8)
        self.rect.midbottom = (x, y)

        self.world_width = GameConfig.LEVEL_WIDTH
    
    def load_animations(self):
        
        frames_dir = GameConfig.asset_path("player_frames")
        self.animations = {
            "idle": self.asset_adapter.load_animation_frames(frames_dir, "idle", 3),
            "walk": self.asset_adapter.load_animation_frames(frames_dir, "walk", 3),
            "jump": self.asset_adapter.load_animation_frames(frames_dir, "jump", 3)
        }
    
    def update(self, input_adapter, delta_time):
        
        dx, dy, jump_pressed = input_adapter.get_movement()
        
        speed = GameConfig.PLAYER_SPEED
        dx *= speed

        self.last_dx = dx

        if self.rect.left + dx < 0:
            dx = max(dx, -self.rect.left)
        if self.rect.right + dx > self.world_width:
            dx = min(dx, self.world_width - self.rect.right)

        if dx < 0:
            self.flip = True
            if self.on_ground: 
                self.action = "walk"
        elif dx > 0:
            self.flip = False
            if self.on_ground: 
                self.action = "walk"
        else:
            if self.on_ground: 
                self.action = "idle"

        if jump_pressed and self.on_ground:
            self.vy = GameConfig.JUMP_STRENGTH
            self.on_ground = False
            self.action = "jump"

        if not self.on_ground and self.vy > 0: 
            self.action = "jump"

        self.vy += GameConfig.GRAVITY
        self.rect.x += dx
        self.rect.y += self.vy

        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vy = 0
            self.on_ground = True

        self.update_animation(delta_time)
    
    def update_animation(self, delta_time):
        anim_len = len(self.animations[self.action])
        self.frame_idx += 15 * delta_time  # Velocidade da animação
        
        if self.action == "jump":
            if self.frame_idx >= anim_len: 
                self.frame_idx = anim_len - 1
        else:
            if self.frame_idx >= anim_len: 
                self.frame_idx = 0
        
        frame_index = int(self.frame_idx)
        if frame_index < len(self.animations[self.action]):
            self.image = self.animations[self.action][frame_index]
    
    def draw(self, graphics_adapter, camera_offset_x=0):
        
        img = self.image
        if self.flip: 
            img = pygame.transform.flip(img, True, False)

        draw_x = self.rect.x - camera_offset_x + (self.rect.width // 2) - (img.get_width() // 2)
        draw_y = self.rect.bottom - img.get_height()
        
        graphics_adapter.draw_sprite(img, draw_x, draw_y)
    
    def get_horizontal_movement(self):
        
        return self.last_dx
    
    def get_state(self):
        
        return {
            "position": (self.rect.x, self.rect.y),
            "action": self.action,
            "flip": self.flip
        }
    
    draw_hitbox = False  
    
    def draw(self, graphics_adapter, camera_offset_x=0):
        
        img = self.image
        if self.flip: 
            img = pygame.transform.flip(img, True, False)

        draw_x = self.rect.x - camera_offset_x + (self.rect.width // 2) - (img.get_width() // 2)
        draw_y = self.rect.bottom - img.get_height()
        
        graphics_adapter.draw_sprite(img, draw_x, draw_y)

        if Player.draw_hitbox:
            debug_rect = pygame.Rect(
                self.rect.x - camera_offset_x,
                self.rect.y,
                self.rect.width,
                self.rect.height
            )
            graphics_adapter.draw_rect((0, 255, 0), debug_rect, 2)