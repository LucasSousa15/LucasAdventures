import pygame
from .state import GameState
from game.entities.player import Player
from game.entities.scenery import Scenery
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
        self.debug_font = pygame.font.Font(None, 36)
    
    def handle_events(self):
        # Verificar se o jogo deve fechar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Voltar ao menu com ESC
                    from .menu_state import MenuState
                    self.change_state(MenuState(self.game))
    
    def update(self, delta_time):
        self.player.update(self.game.input_adapter, delta_time)
        
        # Atualiza cenário com base no movimento do jogador
        player_dx = self.player.get_horizontal_movement()
        self.scenery.update(player_dx)
    
    def render(self):
        # Fundo e cenário
        self.scenery.draw(self.game.graphics_adapter)
        
        # Player (sobre o cenário)
        self.player.draw(self.game.graphics_adapter)
        
        # Debug info
        debug_text = f"Ação: {self.player.action} | Pos: ({self.player.rect.x:.0f}, {self.player.rect.y:.0f})"
        self.game.graphics_adapter.draw_text(debug_text, self.debug_font, 
                                           (255, 255, 255), 10, 10)
        
        self.game.graphics_adapter.update_display()