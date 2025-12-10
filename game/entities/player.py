
import pygame
from game.adapters.asset_adapter import PygameAssetAdapter, FrameNormalizer
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


        self.hitbox_width = int(GameConfig.PLAYER_WIDTH * 0.6)
        self.hitbox_height = int(GameConfig.PLAYER_HEIGHT * 0.7)

        self.rect = pygame.Rect(0, 0, self.hitbox_width, self.hitbox_height)
        self.rect.midbottom = (x, y)


        self.fixed_x = x


        self.draw_hitbox = False


        self.is_dodging = False


        self.is_jumping = False

    def load_animations(self):
        """Carrega e redimensiona animações com garantia de tamanho consistente"""
        frames_dir = GameConfig.asset_path("player_frames")


        idle_frames = self.asset_adapter.load_animation_frames(frames_dir, "idle", 3)
        jump_frames = self.asset_adapter.load_animation_frames(frames_dir, "jump", 3)
        walk_frames = self.asset_adapter.load_animation_frames(frames_dir, "walk", 3)


        try:
            dodge_frame = pygame.image.load(GameConfig.asset_path("player_frames", "jump_2.png")).convert_alpha()
            dodge_frame_normalized = FrameNormalizer.normalize_frame(
                dodge_frame,
                GameConfig.PLAYER_WIDTH,
                GameConfig.PLAYER_HEIGHT,
                maintain_aspect=True,
                align_bottom=True
            )
            dodge_animation = [dodge_frame_normalized]
        except Exception:

            dodge_animation = [self.resize_frames(jump_frames)[1]]


        self.animations = {
            "idle": self.resize_frames(idle_frames),
            "jump": self.resize_frames(jump_frames),
            "run": self.resize_frames(walk_frames),
            "dodge": dodge_animation,
        }


        self._validate_all_frames()

    def _validate_all_frames(self):
        """Valida que todos os frames têm tamanho consistente"""
        for action_name, frames in self.animations.items():
            for idx, frame in enumerate(frames):
                is_valid = FrameNormalizer.validate_frame_size(
                    frame,
                    GameConfig.PLAYER_WIDTH,
                    GameConfig.PLAYER_HEIGHT
                )
                if not is_valid:

                    self.animations[action_name][idx] = FrameNormalizer.normalize_frame(
                        frame,
                        GameConfig.PLAYER_WIDTH,
                        GameConfig.PLAYER_HEIGHT,
                        maintain_aspect=True,
                        align_bottom=True
                    )

    def resize_frames(self, frames):
        """Redimensiona frames para o tamanho configurado com normalização garantida"""
        resized_frames = []
        for frame in frames:


            normalized = FrameNormalizer.normalize_frame(
                frame,
                GameConfig.PLAYER_WIDTH,
                GameConfig.PLAYER_HEIGHT,
                maintain_aspect=True,
                align_bottom=True
            )
            resized_frames.append(normalized)
        return resized_frames

    def update(self, input_adapter, delta_time, game_manager):
        """Atualiza apenas para pulo"""
        keys = pygame.key.get_pressed()


        dodge_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        if dodge_pressed and self.on_ground and not game_manager.is_game_over:
            if not self.is_dodging:
                self.is_dodging = True
                self.action = "dodge"
                self.frame_idx = 0
        else:

            if self.is_dodging:
                self.is_dodging = False
                if not game_manager.is_game_over and not game_manager.is_paused:
                    self.action = "run"
                else:
                    self.action = "idle"


        jump_pressed = False
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            jump_pressed = True


        if jump_pressed and self.on_ground and not game_manager.is_game_over and not self.is_dodging:
            self.vy = GameConfig.JUMP_STRENGTH
            self.on_ground = False
            self.is_jumping = True
            self.action = "jump"


        if not self.is_dodging:
            self.vy += GameConfig.GRAVITY
            self.rect.y += self.vy


            if self.rect.bottom >= self.ground_y:
                self.rect.bottom = self.ground_y
                self.vy = 0
                self.on_ground = True
                self.is_jumping = False


                if not game_manager.is_game_over and not game_manager.is_paused:
                    self.action = "run"
                else:
                    self.action = "idle"
        else:

            self.rect.bottom = self.ground_y
            self.vy = 0


        self.update_animation(delta_time)

    def update_animation(self, delta_time):
        anim_len = len(self.animations[self.action])

        if self.action == "dodge":

            self.frame_idx = 0
        else:
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
        """Desenha o jogador com garantia de tamanho consistente"""
        img = self.image


        if not FrameNormalizer.validate_frame_size(img, GameConfig.PLAYER_WIDTH, GameConfig.PLAYER_HEIGHT):
            img = FrameNormalizer.normalize_frame(
                img,
                GameConfig.PLAYER_WIDTH,
                GameConfig.PLAYER_HEIGHT,
                maintain_aspect=True
            )
            self.image = img

        draw_x = self.fixed_x - img.get_width() // 2
        draw_y = self.rect.bottom - img.get_height()

        graphics_adapter.draw_sprite(img, draw_x, draw_y)



        show_hit = self.draw_hitbox or getattr(GameConfig, "DEBUG_SHOW_COLLISIONS", False)
        if show_hit:
            debug_rect = pygame.Rect(
                self.rect.x,
                self.rect.y,
                self.rect.width,
                self.rect.height
            )
            graphics_adapter.draw_rect((0, 255, 0), debug_rect, 2)


            size_text = f"{img.get_width()}x{img.get_height()}"
            font = pygame.font.Font(None, 20)
            text_surf = font.render(size_text, True, (255, 255, 255))
            graphics_adapter.screen.blit(text_surf, (draw_x, draw_y - 20))
