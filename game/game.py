
import pygame
from game.adapters import KeyboardInputAdapter, PygameGraphicsAdapter, PygameAssetAdapter
from game.utils.config import GameConfig

class Game:
    def __init__(self):

        self.graphics_adapter = PygameGraphicsAdapter()
        self.input_adapter = KeyboardInputAdapter()
        self.asset_adapter = PygameAssetAdapter()

        self.screen = self.graphics_adapter.init_display(
            GameConfig.SCREEN_WIDTH,
            GameConfig.SCREEN_HEIGHT,
            "Lucas Adventure - Demo"
        )

        from game.states.menu_state import MenuState
        self.running = True
        self.state = MenuState(self)
    
    def change_state(self, new_state):
        self.state = new_state
    
    def run(self):
        while self.running:
            delta_time = self.graphics_adapter.get_delta_time()

            self.state.handle_events()

            self.state.update(delta_time)

            self.state.render()
        
        pygame.quit()