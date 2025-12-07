
import pygame
import random
from .state import GameState
from game.entities.player import Player
from game.entities.scenery import Scenery
from game.entities.camera import Camera
from game.entities.coin_manager import CoinManager
from game.utils.config import GameConfig

class GameState(GameState):
    def __init__(self, game):
        super().__init__(game)

        self.player = Player(
            GameConfig.SCREEN_WIDTH // 2,
            GameConfig.GROUND_LEVEL,
            self.game.asset_adapter
        )

        self.scenery = Scenery(self.game.asset_adapter)

        self.camera = Camera()

        self.coin_manager = CoinManager(self.game.asset_adapter)

        self.debug_font = pygame.font.Font(None, 36)
        self.ui_font = pygame.font.Font(None, 48)
        self.large_font = pygame.font.Font(None, 72)

        self.coin_collect_effect = 0
        self.combo_counter = 0
        self.last_coin_time = 0
        self.combo_text = ""
        self.combo_timer = 0

        self.game_time = 0

        self.show_tutorial = True
        self.tutorial_timer = 300  # 5 segundos a 60 FPS

        self.start_effect = 60  # 1 segundo a 60 FPS
        
    def handle_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    from .menu_state import MenuState
                    self.change_state(MenuState(self.game))
                
                elif event.key == pygame.K_r:

                    self.coin_manager.reset()
                    self.combo_counter = 0
                    self.combo_text = ""
                
                elif event.key == pygame.K_t:

                    for _ in range(10):
                        if self.coin_manager.coins:
                            coin = self.coin_manager.coins[0]
                            if not coin.collected:
                                coin.collect()
                                self.coin_manager.total_score += GameConfig.COIN_VALUE
                
                elif event.key == pygame.K_h:

                    self.show_tutorial = not self.show_tutorial
                
                elif event.key == pygame.K_F1:

                    Player.draw_hitbox = not getattr(Player, 'draw_hitbox', False)
    
    def update(self, delta_time):
        

        self.game_time += delta_time

        self.player.update(self.game.input_adapter, delta_time)

        self.camera.update(self.player)

        camera_offset_x = self.camera.get_offset_x()
        self.scenery.update(camera_offset_x)

        collected = self.coin_manager.update(self.player.rect, delta_time)

        if collected > 0:

            self.coin_collect_effect = 25  # Duração do efeito em frames

            current_time = pygame.time.get_ticks()
            if current_time - self.last_coin_time < 1000:  # Combo se coletar em menos de 1 segundo
                self.combo_counter += 1
                if self.combo_counter >= 5:
                    self.combo_text = f"COMBO x{self.combo_counter}!"
                    self.coin_manager.total_score += (self.combo_counter - 1) * 5  # Bônus de combo
                self.combo_timer = 60  # Mostrar combo por 1 segundo
            else:
                self.combo_counter = 1
            
            self.last_coin_time = current_time

        if self.coin_collect_effect > 0:
            self.coin_collect_effect -= 1
        
        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer == 0:
                self.combo_text = ""
        
        if self.show_tutorial and self.tutorial_timer > 0:
            self.tutorial_timer -= 1
        
        if self.start_effect > 0:
            self.start_effect -= 1

        if self.coin_manager.get_remaining_coins() == 0 and len(self.coin_manager.coins) > 0:

            pass
    
    def render(self):
        

        self.game.graphics_adapter.clear(GameConfig.SKY_BLUE)

        camera_offset_x = self.camera.get_offset_x()

        self.scenery.draw(self.game.graphics_adapter, camera_offset_x)

        self.coin_manager.draw(self.game.graphics_adapter, camera_offset_x)

        self.player.draw(self.game.graphics_adapter, camera_offset_x)

        if self.coin_collect_effect > 0:
            self.draw_coin_collect_effect()

        if self.start_effect > 0:
            self.draw_start_effect()

        self.draw_ui(camera_offset_x)

        self.draw_debug_info()

        self.game.graphics_adapter.update_display()
    
    def draw_coin_collect_effect(self):
        
        alpha = min(255, self.coin_collect_effect * 10)
        size = self.coin_collect_effect * 3

        player_screen_x = self.player.rect.centerx - self.camera.get_offset_x()
        player_screen_y = self.player.rect.centery

        effect_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(effect_surf, (255, 215, 0, alpha // 2), 
                          (size, size), size)
        pygame.draw.circle(effect_surf, (255, 255, 200, alpha), 
                          (size, size), size // 2)

        self.game.graphics_adapter.screen.blit(
            effect_surf, 
            (player_screen_x - size, player_screen_y - size)
        )
    
    def draw_start_effect(self):
        
        alpha = min(255, self.start_effect * 4)

        fade_surf = pygame.Surface((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        fade_surf.fill((0, 0, 0))
        fade_surf.set_alpha(alpha)

        self.game.graphics_adapter.screen.blit(fade_surf, (0, 0))
    
    def draw_ui(self, camera_offset_x):
        
        score = self.coin_manager.get_score()
        remaining = self.coin_manager.get_remaining_coins()
        total = self.coin_manager.get_total_coins()

        score_text = f"Pontuação: {score}"
        score_surface = self.ui_font.render(score_text, True, (255, 215, 0))

        coins_text = f"Moedas: {total - remaining}/{total}"
        coins_surface = self.ui_font.render(coins_text, True, (255, 215, 0))

        score_rect = score_surface.get_rect(topright=(GameConfig.SCREEN_WIDTH - 20, 20))
        coins_rect = coins_surface.get_rect(topright=(GameConfig.SCREEN_WIDTH - 20, 80))

        pygame.draw.rect(
            self.game.graphics_adapter.screen, 
            (0, 0, 0, 180),
            score_rect.inflate(20, 10),
            border_radius=10
        )
        
        pygame.draw.rect(
            self.game.graphics_adapter.screen,
            (0, 0, 0, 180),
            coins_rect.inflate(20, 10),
            border_radius=10
        )

        self.game.graphics_adapter.screen.blit(score_surface, score_rect)
        self.game.graphics_adapter.screen.blit(coins_surface, coins_rect)

        if self.combo_timer > 0 and self.combo_text:
            combo_color = (
                min(255, 100 + self.combo_counter * 20),
                min(255, 215 + self.combo_counter * 5),
                0
            )
            
            combo_surface = self.large_font.render(self.combo_text, True, combo_color)
            combo_rect = combo_surface.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 150))

            shadow_surface = self.large_font.render(self.combo_text, True, (0, 0, 0))
            self.game.graphics_adapter.screen.blit(shadow_surface, combo_rect.move(3, 3))

            self.game.graphics_adapter.screen.blit(combo_surface, combo_rect)

        if self.show_tutorial and self.tutorial_timer > 0:
            self.draw_tutorial()

        self.draw_instructions()
    
    def draw_tutorial(self):
        
        tutorial_lines = [
            "Colete todas as moedas!",
            "Use ← → para se mover",
            "Espaço para pular",
            "Tente pegar moedas seguidas para combos!",
            "(Tutorial some em " + str(self.tutorial_timer // 60) + "s)"
        ]

        tutorial_height = len(tutorial_lines) * 40 + 40
        pygame.draw.rect(
            self.game.graphics_adapter.screen,
            (0, 0, 0, 200),
            (GameConfig.SCREEN_WIDTH // 2 - 250, 250, 500, tutorial_height),
            border_radius=15
        )

        title = self.ui_font.render("TUTORIAL", True, (255, 215, 0))
        title_rect = title.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 280))
        self.game.graphics_adapter.screen.blit(title, title_rect)

        for i, line in enumerate(tutorial_lines):
            text = self.debug_font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 330 + i * 40))
            self.game.graphics_adapter.screen.blit(text, text_rect)
    
    def draw_instructions(self):
        
        instructions = [
            "ESC: Menu | ←→: Mover | Espaço: Pular",
            "R: Resetar moedas | F1: Hitboxes (DEBUG)"
        ]
        
        for i, line in enumerate(instructions):
            self.game.graphics_adapter.draw_text(
                line, 
                self.debug_font,
                (200, 200, 200), 
                10, 
                GameConfig.SCREEN_HEIGHT - 60 + i * 30
            )

        progress = self.coin_manager.get_remaining_coins()
        if progress <= 5:
            warning = f"Apenas {progress} moeda(s) restante(s)!"
            warning_surface = self.ui_font.render(warning, True, (255, 100, 100))
            warning_rect = warning_surface.get_rect(midbottom=(GameConfig.SCREEN_WIDTH // 2, GameConfig.SCREEN_HEIGHT - 100))

            pygame.draw.rect(
                self.game.graphics_adapter.screen,
                (0, 0, 0, 180),
                warning_rect.inflate(30, 15),
                border_radius=10
            )
            
            self.game.graphics_adapter.screen.blit(warning_surface, warning_rect)
    
    def draw_debug_info(self):
        
        debug_info = [
            f"Posição: ({self.player.rect.x:.0f}, {self.player.rect.y:.0f})",
            f"Câmera: {self.camera.get_offset_x():.0f}",
            f"Player Action: {self.player.action}",
            f"Moedas ativas: {len(self.coin_manager.coins)}",
            f"Tempo: {self.game_time:.1f}s",
            f"FPS: {int(1/self.game.graphics_adapter.get_delta_time() if self.game.graphics_adapter.get_delta_time() > 0 else 0)}"
        ]
        
        for i, info in enumerate(debug_info):
            self.game.graphics_adapter.draw_text(
                info,
                self.debug_font,
                (200, 255, 200),
                10,
                10 + i * 30
            )

        if self.coin_manager.get_remaining_coins() == 0 and len(self.coin_manager.coins) > 0:
            completed_text = "Todas as moedas coletadas! Pressione R para reiniciar."
            self.game.graphics_adapter.draw_text(
                completed_text,
                self.ui_font,
                (100, 255, 100),
                GameConfig.SCREEN_WIDTH // 2 - 300,
                GameConfig.SCREEN_HEIGHT // 2
            )