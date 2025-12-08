# game/states/game_state.py (versão runner)
import pygame
from .state import GameState
from game.entities.player import Player
from game.entities.scenery import Scenery
from game.entities.game_manager import GameManager
from game.utils.config import GameConfig

class GameState(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Jogador no centro inferior
        self.player = Player(
            GameConfig.SCREEN_WIDTH // 2,
            GameConfig.GROUND_LEVEL,
            self.game.asset_adapter
        )
        
        # Cenário com movimento
        self.scenery = Scenery(self.game.asset_adapter)
        
        # Gerenciador do jogo (substitui coin_manager e enemy_manager)
        self.game_manager = GameManager(self.game.asset_adapter)
        
        # Fontes
        self.debug_font = pygame.font.Font(None, 36)
        self.ui_font = pygame.font.Font(None, 48)
        self.large_font = pygame.font.Font(None, 72)
        
        # Tutorial
        self.show_instructions = True
        self.instruction_timer = 300  # 5 segundos
    
    def handle_events(self):
        """Processa eventos de entrada"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from .menu_state import MenuState
                    self.change_state(MenuState(self.game))
                
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    # Restart no game over
                    if self.game_manager.is_game_over:
                        self.game_manager.reset()
                        self.player.action = "run"
                
                elif event.key == pygame.K_p:
                    # Pause/play
                    if not self.game_manager.is_game_over:
                        self.game_manager.toggle_pause()
                
                elif event.key == pygame.K_F1:
                    # Debug: mostrar hitboxes
                    self.player.draw_hitbox = not self.player.draw_hitbox
                
                elif event.key == pygame.K_h:
                    # Mostrar/ocultar instruções
                    self.show_instructions = not self.show_instructions
    
    def update(self, delta_time):
        """Atualiza lógica do jogo"""
        # Atualiza jogador
        self.player.update(self.game.input_adapter, delta_time, self.game_manager)
        
        # Atualiza cenário
        self.scenery.update(self.game_manager.game_speed)
        
        # Atualiza gerenciador do jogo
        self.game_manager.update(delta_time, self.player.rect)
        
        # Atualiza timer das instruções
        if self.instruction_timer > 0:
            self.instruction_timer -= 1
    
    def render(self):
        """Renderiza o jogo"""
        # Limpa a tela
        self.game.graphics_adapter.clear(GameConfig.SKY_BLUE)
        
        # Desenha cenário
        self.scenery.draw(self.game.graphics_adapter)
        
        # Desenha obstáculos
        self.game_manager.draw(self.game.graphics_adapter)
        
        # Desenha jogador
        self.player.draw(self.game.graphics_adapter)
        
        # Desenha UI
        self.game_manager.draw_ui(self.game.graphics_adapter, 
                                 self.ui_font, self.large_font)
        
        # Desenha instruções
        if self.show_instructions and self.instruction_timer > 0:
            self.draw_instructions()
        
        # Desenha controles permanentes
        self.draw_controls()
        
        # Atualiza tela
        self.game.graphics_adapter.update_display()
    
    def draw_instructions(self):
        """Desenha instruções iniciais"""
        instructions = [
            "LUCAS RUNNER",
            "",
            "Controles:",
            "ESPAÇO ou ↑ - Pular",
            "P - Pausar/Continuar",
            "ESC - Menu",
            "",
            "Evite os obstáculos!",
            f"Instruções desaparecem em {self.instruction_timer//60}s"
        ]
        
        # Fundo
        width, height = 500, 350
        x = GameConfig.SCREEN_WIDTH // 2 - width // 2
        y = GameConfig.SCREEN_HEIGHT // 2 - height // 2
        
        pygame.draw.rect(self.game.graphics_adapter.screen,
                        (0, 0, 0, 200),
                        (x, y, width, height),
                        border_radius=15)
        
        # Textos
        for i, line in enumerate(instructions):
            color = (255, 215, 0) if i == 0 else (255, 255, 255)
            font = self.large_font if i == 0 else self.ui_font
            text_surf = font.render(line, True, color)
            text_rect = text_surf.get_rect(center=(GameConfig.SCREEN_WIDTH//2, 
                                                  y + 50 + i * 40))
            self.game.graphics_adapter.screen.blit(text_surf, text_rect)
    
    def draw_controls(self):
        """Desenha controles na tela"""
        controls = [
            "P: Pausa  |  F1: Hitboxes  |  H: Instruções"
        ]
        
        for i, line in enumerate(controls):
            self.game.graphics_adapter.draw_text(
                line, 
                self.debug_font,
                (150, 150, 150), 
                10, 
                GameConfig.SCREEN_HEIGHT - 30
            )