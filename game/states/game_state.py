
import pygame
from .state import GameState
from game.entities.player import Player
from game.utils.config import GameConfig

class GameState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player(
            GameConfig.SCREEN_WIDTH // 2,
            GameConfig.GROUND_LEVEL,
            self.game.asset_adapter
        )
        self.debug_font = pygame.font.Font(None, 36)
    
    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    from .menu_state import MenuState
                    self.change_state(MenuState(self.game))
    
    def update(self, delta_time):
        self.player.update(self.game.input_adapter, delta_time)
    
    def render(self):

        self.game.graphics_adapter.clear(GameConfig.SKY_BLUE)

        ground_rect = pygame.Rect(0, GameConfig.GROUND_LEVEL, 
                                 GameConfig.SCREEN_WIDTH, 
                                 GameConfig.SCREEN_HEIGHT - GameConfig.GROUND_LEVEL)
        self.game.graphics_adapter.draw_rect(GameConfig.GROUND_GREEN, ground_rect)

        self.player.draw(self.game.graphics_adapter)

        debug_text = f"Ação: {self.player.action} | Pos: ({self.player.rect.x:.0f}, {self.player.rect.y:.0f})"
        self.game.graphics_adapter.draw_text(debug_text, self.debug_font, 
                                           GameConfig.BLACK, 10, 10)
        
        self.game.graphics_adapter.update_display()