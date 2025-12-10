
import pygame
from .state import GameState
from game.entities.player import Player
from game.entities.scenery import Scenery
from game.entities.game_manager import GameManager
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


        self.game_manager = GameManager(self.game.asset_adapter)


        self.debug_font = pygame.font.Font(None, 36)
        self.ui_font = pygame.font.Font(None, 48)
        self.large_font = pygame.font.Font(None, 72)


        self.show_instructions = True
        self.instruction_timer = 300

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

                    if self.game_manager.is_game_over:
                        self.game_manager.reset()
                        self.player.action = "run"

                elif event.key == pygame.K_p:

                    if not self.game_manager.is_game_over:
                        self.game_manager.toggle_pause()

                elif event.key == pygame.K_F1:

                    from game.utils.config import GameConfig
                    current = getattr(GameConfig, "DEBUG_SHOW_COLLISIONS", False)
                    GameConfig.DEBUG_SHOW_COLLISIONS = not current

                    self.player.draw_hitbox = GameConfig.DEBUG_SHOW_COLLISIONS

                elif event.key == pygame.K_h:

                    self.show_instructions = not self.show_instructions

    def update(self, delta_time):
        """Atualiza lógica do jogo"""

        self.player.update(self.game.input_adapter, delta_time, self.game_manager)


        self.scenery.update(self.game_manager.game_speed)


        self.game_manager.update(delta_time, self.player)


        if self.instruction_timer > 0:
            self.instruction_timer -= 1

    def render(self):
        """Renderiza o jogo"""

        self.game.graphics_adapter.clear(GameConfig.SKY_BLUE)


        self.scenery.draw(self.game.graphics_adapter)


        self.game_manager.draw(self.game.graphics_adapter)


        self.player.draw(self.game.graphics_adapter)


        self.game_manager.draw_ui(self.game.graphics_adapter,
                                 self.ui_font, self.large_font)


        if self.show_instructions and self.instruction_timer > 0:
            self.draw_instructions()


        self.draw_controls()


        self.game.graphics_adapter.update_display()

    def draw_instructions(self):
        """Desenha instruções iniciais"""
        instructions = [
            "LUCAS RUNNER",
            "",
            "Controles:",
            "ESPAÇO ou ↑ - Pular",
            "SHIFT - Esquivar (no chão)",
            "P - Pausar/Continuar",
            "ESC - Menu",
            "",
            "Evite os obstáculos!",
            f"Instruções desaparecem em {self.instruction_timer//60}s"
        ]


        width, height = 500, 400
        x = GameConfig.SCREEN_WIDTH // 2 - width // 2
        y = GameConfig.SCREEN_HEIGHT // 2 - height // 2

        pygame.draw.rect(self.game.graphics_adapter.screen,
                        (0, 0, 0, 200),
                        (x, y, width, height),
                        border_radius=15)


        for i, line in enumerate(instructions):
            color = (255, 215, 0) if i == 0 else (255, 255, 255)
            font = self.large_font if i == 0 else self.ui_font
            text_surf = font.render(line, True, color)
            text_rect = text_surf.get_rect(center=(GameConfig.SCREEN_WIDTH//2,
                                                  y + 50 + i * 35))
            self.game.graphics_adapter.screen.blit(text_surf, text_rect)

    def draw_controls(self):
        """Desenha controles na tela"""
        controls = [
            "ESPAÇO: Pula  |  SHIFT: Esquiva  |  P: Pausa  |  F1: Hitboxes  |  H: Instruções"
        ]

        for i, line in enumerate(controls):
            self.game.graphics_adapter.draw_text(
                line,
                self.debug_font,
                (150, 150, 150),
                10,
                GameConfig.SCREEN_HEIGHT - 30
            )
