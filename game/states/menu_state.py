
import pygame
from .state import GameState
from game.utils.config import GameConfig

class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.selected_option = 0
        self.options = ["Jogar", "Controles", "Sair"]
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
    
    def handle_events(self):
        if self.game.input_adapter.should_quit():
            self.game.running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()
                elif event.key == pygame.K_ESCAPE:
                    self.game.running = False
    
    def select_option(self):
        if self.selected_option == 0:  

            from .game_state import GameState as PlayState
            self.change_state(PlayState(self.game))
        elif self.selected_option == 1:  

            print("Mostrando controles...")
        elif self.selected_option == 2:  
            self.game.running = False
    
    def update(self, delta_time):
        pass
    
    def render(self):

        self.game.graphics_adapter.clear(GameConfig.SKY_BLUE)

        title = self.font.render("LUCAS ADVENTURE", True, (255, 215, 0))
        title_rect = title.get_rect(center=(GameConfig.SCREEN_WIDTH//2, 200))
        self.game.graphics_adapter.draw_sprite(title, title_rect.x, title_rect.y)

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (200, 200, 200)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(GameConfig.SCREEN_WIDTH//2, 400 + i*100))
            self.game.graphics_adapter.draw_sprite(text, text_rect.x, text_rect.y)

        controls = [
            "← → : Mover",
            "ESPAÇO : Pular",
            "ENTER : Selecionar",
            "ESC : Voltar/Sair"
        ]
        
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, (255, 255, 255))
            self.game.graphics_adapter.draw_sprite(text, 50, 800 + i*40)
        
        self.game.graphics_adapter.update_display()