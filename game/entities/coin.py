
import pygame
import random
import math
from game.utils.config import GameConfig

class Coin:
    def __init__(self, x, y, asset_adapter):
        self.asset_adapter = asset_adapter
        self.load_animation_frames()

        self.x = x
        self.y = y

        self.frame_idx = 0.0
        self.current_frame = self.frames[0]

        self.hitbox_size = int(GameConfig.COIN_SIZE * 0.8)  # 80% do tamanho visual
        self.rect = pygame.Rect(0, 0, self.hitbox_size, self.hitbox_size)
        self.rect.center = (x, y)

        self.collected = False
        self.collection_time = 0
        self.collection_duration = 300  # ms para desaparecer após coleta

        self.float_offset = random.uniform(0, math.pi * 2)  # Fase aleatória
        self.float_amplitude = 5  # Poucos pixels de flutuação
        self.float_speed = 2.0  # Velocidade da flutuação
        
    def load_animation_frames(self):
        
        frames_dir = GameConfig.asset_path("coin")
        self.frames = []
        
        print(f"Carregando moedas de: {frames_dir}")

        for i in range(5):
            frame_path = f"{frames_dir}/{i}.png"
            try:
                if self.asset_adapter and hasattr(self.asset_adapter, 'load_image'):
                    frame = self.asset_adapter.load_image(frame_path)

                    frame = pygame.transform.scale(frame, 
                        (GameConfig.COIN_SIZE, GameConfig.COIN_SIZE))
                    self.frames.append(frame)
                    print(f"✓ Frame {i}.png carregado ({GameConfig.COIN_SIZE}x{GameConfig.COIN_SIZE})")
                else:
                    raise Exception("Asset adapter não disponível")
            except Exception as e:

                print(f"✗ Erro ao carregar moeda {i}.png: {e}")
                self.frames.append(self.create_fallback_coin())

        if not self.frames:
            print("⚠️ Usando moedas de fallback")
            for i in range(5):
                self.frames.append(self.create_fallback_coin())
    
    def create_fallback_coin(self):
        
        size = GameConfig.COIN_SIZE
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        center = (size // 2, size // 2)
        radius = size // 2 - 2

        colors = [
            (255, 215, 0),    # Dourado externo
            (255, 230, 100),  # Dourado médio
            (255, 255, 150),  # Dourado claro
            (255, 240, 120),  # Dourado
            (200, 170, 0)     # Dourado escuro
        ]
        
        for i, color in enumerate(colors):
            r = radius * (1 - i * 0.15)
            pygame.draw.circle(surf, color, center, int(r))

        pygame.draw.circle(surf, (255, 255, 200), center, int(radius * 0.3))

        pygame.draw.circle(surf, (255, 255, 255, 180), 
                          (center[0] - radius//3, center[1] - radius//3), 
                          radius // 5)
        
        return surf
    
    def update(self, delta_time):
        
        if not self.collected:

            self.frame_idx += GameConfig.COIN_ANIMATION_SPEED * delta_time * 60
            if self.frame_idx >= len(self.frames):
                self.frame_idx = 0
            
            self.current_frame = self.frames[int(self.frame_idx)]

            self.float_offset += self.float_speed * delta_time
        else:

            self.collection_time += delta_time * 1000
    
    def collect(self):
        
        if not self.collected:
            self.collected = True
            self.collection_time = 0
            return True
        return False
    
    def should_remove(self):
        
        return self.collected and self.collection_time >= self.collection_duration
    
    def get_draw_y(self):
        

        return self.y + math.sin(self.float_offset) * self.float_amplitude
    
    def draw(self, graphics_adapter, camera_offset_x):
        
        if not self.collected or self.collection_time < self.collection_duration:

            alpha = 255
            scale = 1.0
            
            if self.collected:

                progress = self.collection_time / self.collection_duration
                alpha = max(0, 255 - int(255 * progress))
                scale = max(0.3, 1.0 - progress * 0.7)

            if self.collected and scale < 1.0:
                new_size = int(GameConfig.COIN_SIZE * scale)
                current_frame = pygame.transform.scale(
                    self.current_frame, 
                    (new_size, new_size)
                )
                current_frame.set_alpha(alpha)
            else:
                current_frame = self.current_frame
                if self.collected:
                    current_frame.set_alpha(alpha)

            draw_x = self.x - camera_offset_x - current_frame.get_width() // 2
            draw_y = self.get_draw_y() - current_frame.get_height() // 2
            
            graphics_adapter.draw_sprite(current_frame, draw_x, draw_y)

            if self.collected:
                self.current_frame.set_alpha(255)
    
    def get_rect(self):
        

        return pygame.Rect(
            self.x - self.hitbox_size // 2,
            self.y - self.hitbox_size // 2,
            self.hitbox_size,
            self.hitbox_size
        )