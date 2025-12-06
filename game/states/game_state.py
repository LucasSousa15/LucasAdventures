
import pygame
from .state import GameState
from game.entities.player import Player
from game.entities.scenery import Scenery
from game.entities.camera import Camera
from game.utils.config import GameConfig

class GameState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player(
            GameConfig.SCREEN_WIDTH // 2,  # Posição inicial X
            GameConfig.GROUND_LEVEL,
            self.game.asset_adapter
        )
        self.scenery = Scenery(self.game.asset_adapter)
        self.camera = Camera()
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

        self.camera.update(self.player)

        camera_offset_x = self.camera.get_offset_x()
        self.scenery.update(camera_offset_x)
    
    def render(self):

        self.game.graphics_adapter.clear(GameConfig.SKY_BLUE)

        camera_offset_x = self.camera.get_offset_x()

        self.scenery.draw(self.game.graphics_adapter, camera_offset_x)

        self.player.draw(self.game.graphics_adapter, camera_offset_x)

        debug_text = f"Pos: ({self.player.rect.x:.0f}, {self.player.rect.y:.0f}) | Camera: {camera_offset_x:.0f}/{GameConfig.LEVEL_WIDTH}"
        self.game.graphics_adapter.draw_text(debug_text, self.debug_font, 
                                           (255, 255, 255), 10, 10)

        instructions = "ESC: Menu | ←→: Mover | Espaço: Pular"
        self.game.graphics_adapter.draw_text(instructions, self.debug_font,
                                           (255, 255, 255), 10, 50)
        
        self.game.graphics_adapter.update_display()