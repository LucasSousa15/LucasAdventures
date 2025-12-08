# game/entities/player.py (versão com tamanho corrigido)
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
        
        # Física
        self.vy = 0
        self.on_ground = True
        
        # Hitbox PROPORCIONAL ao tamanho do sprite
        self.hitbox_width = int(GameConfig.PLAYER_WIDTH * 0.6)
        self.hitbox_height = int(GameConfig.PLAYER_HEIGHT * 0.7)
        
        self.rect = pygame.Rect(0, 0, self.hitbox_width, self.hitbox_height)
        self.rect.midbottom = (x, y)
        
        # Para runner: jogador fica sempre na mesma posição X
        self.fixed_x = x
        
        # Variável para controlar hitbox debug
        self.draw_hitbox = False
        
        print(f"✅ Jogador criado: {GameConfig.PLAYER_WIDTH}x{GameConfig.PLAYER_HEIGHT}px")
        print(f"   Hitbox: {self.hitbox_width}x{self.hitbox_height}px")
    
    def load_animations(self):
        """Carrega e redimensiona animações"""
        frames_dir = GameConfig.asset_path("player_frames")
        
        # Carrega frames originais
        idle_frames = self.asset_adapter.load_animation_frames(frames_dir, "idle", 3)
        jump_frames = self.asset_adapter.load_animation_frames(frames_dir, "jump", 3)
        walk_frames = self.asset_adapter.load_animation_frames(frames_dir, "walk", 3)
        
        # Redimensiona todos os frames para tamanho do jogador
        self.animations = {
            "idle": self.resize_frames(idle_frames),
            "jump": self.resize_frames(jump_frames),
            "run": self.resize_frames(walk_frames),  # Usa walk como run
        }
        
        print(f"✅ Frames redimensionados para {GameConfig.PLAYER_WIDTH}x{GameConfig.PLAYER_HEIGHT}")
    
    def resize_frames(self, frames):
        """Redimensiona frames para o tamanho configurado"""
        resized_frames = []
        for frame in frames:
            # Redimensiona mantendo proporção
            resized = pygame.transform.scale(
                frame, 
                (GameConfig.PLAYER_WIDTH, GameConfig.PLAYER_HEIGHT)
            )
            resized_frames.append(resized)
        return resized_frames
    
    def update(self, input_adapter, delta_time, game_manager):
        """Atualiza apenas para pulo"""
        # Verifica se está no chão e pulo pressionado
        jump_pressed = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            jump_pressed = True
        
        # Pulo
        if jump_pressed and self.on_ground and not game_manager.is_game_over:
            self.vy = GameConfig.JUMP_STRENGTH
            self.on_ground = False
            self.action = "jump"
        
        # Aplica gravidade
        self.vy += GameConfig.GRAVITY
        self.rect.y += self.vy
        
        # Colisão com o chão
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vy = 0
            self.on_ground = True
            
            # Animação de corrida quando no chão
            if not game_manager.is_game_over and not game_manager.is_paused:
                self.action = "run"
            else:
                self.action = "idle"
        
        # Atualiza animação
        self.update_animation(delta_time)
    
    def update_animation(self, delta_time):
        anim_len = len(self.animations[self.action])
        self.frame_idx += 15 * delta_time
        
        if self.action == "jump":
            if self.frame_idx >= anim_len:
                self.frame_idx = anim_len - 1
        else:
            if self.frame_idx >= anim_len:
                self.frame_idx = 0
        
        frame_index = int(self.frame_idx)
        if frame_index < len(self.animations[self.action]):
            self.image = self.animations[self.action][frame_index]
    
    def draw(self, graphics_adapter):
        """Desenha o jogador"""
        img = self.image
        draw_x = self.fixed_x - img.get_width() // 2
        draw_y = self.rect.bottom - img.get_height()
        
        graphics_adapter.draw_sprite(img, draw_x, draw_y)
        
        # Debug: mostra hitbox
        if self.draw_hitbox:
            debug_rect = pygame.Rect(
                self.rect.x,
                self.rect.y,
                self.rect.width,
                self.rect.height
            )
            graphics_adapter.draw_rect((0, 255, 0), debug_rect, 2)
            
            # Mostra tamanho
            size_text = f"{img.get_width()}x{img.get_height()}"
            font = pygame.font.Font(None, 20)
            text_surf = font.render(size_text, True, (255, 255, 255))
            graphics_adapter.screen.blit(text_surf, (draw_x, draw_y - 20))