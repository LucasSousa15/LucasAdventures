# game/game.py
import pygame
from game.adapters import KeyboardInputAdapter, PygameGraphicsAdapter, PygameAssetAdapter, PygameAudioAdapter
from game.utils.config import GameConfig

class Game:
    def __init__(self):
        # Inicializa os adapters
        self.graphics_adapter = PygameGraphicsAdapter()
        self.input_adapter = KeyboardInputAdapter()
        self.asset_adapter = PygameAssetAdapter()
        # self.audio_adapter = PygameAudioAdapter()  
        
        # Configura a tela
        self.screen = self.graphics_adapter.init_display(
            GameConfig.SCREEN_WIDTH,
            GameConfig.SCREEN_HEIGHT,
            "Lucas Adventure - Coletáveis"
        )
        
        # Toca música de fundo (opcional)
        # self.audio_adapter.play_music("background", volume=0.3)
        
        # Estado do jogo
        from game.states.menu_state import MenuState
        self.running = True
        self.state = MenuState(self)
    
    def change_state(self, new_state):
        self.state = new_state
    
    def run(self):
        while self.running:
            delta_time = self.graphics_adapter.get_delta_time()
            
            # Processa eventos
            self.state.handle_events()
            
            # Atualiza lógica
            self.state.update(delta_time)
            
            # Renderiza
            self.state.render()
        
        pygame.quit()