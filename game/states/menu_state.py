# game/states/menu_state.py (adaptado)
import pygame
from .state import GameState
from game.utils.config import GameConfig

class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.selected_option = 0
        self.options = ["Jogar", "Instruções", "Sair"]
        self.title_font = pygame.font.Font(None, 96)
        self.option_font = pygame.font.Font(None, 64)
        self.instruction_font = pygame.font.Font(None, 36)
        
        # Modo de instruções
        self.show_instructions = False
    
    def handle_events(self):
        """Processa entrada no menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.show_instructions:
                    # Qualquer tecla volta do menu de instruções
                    self.show_instructions = False
                
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.select_option()
                
                elif event.key == pygame.K_ESCAPE:
                    self.game.running = False
    
    def select_option(self):
        """Seleciona a opção atual"""
        if self.selected_option == 0:  # Jogar
            from .game_state import GameState as PlayState
            self.change_state(PlayState(self.game))
        
        elif self.selected_option == 1:  # Instruções
            self.show_instructions = True
        
        elif self.selected_option == 2:  # Sair
            self.game.running = False
    
    def update(self, delta_time):
        """Atualiza animações do menu"""
        pass
    
    def render(self):
        """Renderiza o menu"""
        # Fundo
        self.game.graphics_adapter.clear((30, 30, 40))
        
        if self.show_instructions:
            self.render_instructions()
        else:
            self.render_main_menu()
        
        self.game.graphics_adapter.update_display()
    
    def render_main_menu(self):
        """Renderiza o menu principal"""
        # Título
        title = self.title_font.render("LUCAS RUNNER", True, (255, 215, 0))
        title_rect = title.get_rect(center=(GameConfig.SCREEN_WIDTH//2, 150))
        self.game.graphics_adapter.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.instruction_font.render("Estilo Chrome Dino", True, (200, 200, 255))
        subtitle_rect = subtitle.get_rect(center=(GameConfig.SCREEN_WIDTH//2, 230))
        self.game.graphics_adapter.screen.blit(subtitle, subtitle_rect)
        
        # Opções
        for i, option in enumerate(self.options):
            color = (255, 255, 100) if i == self.selected_option else (200, 200, 200)
            text = self.option_font.render(option, True, color)
            text_rect = text.get_rect(center=(GameConfig.SCREEN_WIDTH//2, 350 + i*100))
            self.game.graphics_adapter.screen.blit(text, text_rect)
        
        # Controles
        controls = [
            "↑↓ : Navegar",
            "ENTER/ESPAÇO : Selecionar",
            "ESC : Sair"
        ]
        
        for i, control in enumerate(controls):
            text = self.instruction_font.render(control, True, (150, 150, 200))
            self.game.graphics_adapter.screen.blit(text, (50, GameConfig.SCREEN_HEIGHT - 150 + i*40))
    
    def render_instructions(self):
        """Renderiza tela de instruções"""
        instructions = [
            "=== INSTRUÇÕES ===",
            "",
            "Objetivo:",
            "• Pule sobre os obstáculos",
            "• Quanto mais longe, maior a pontuação",
            "• A velocidade aumenta com o tempo",
            "",
            "Controles:",
            "• ESPAÇO ou SETA ↑ : Pular",
            "• P : Pausar/Continuar",
            "• ESC : Voltar ao menu",
            "",
            "Obstáculos:",
            "• CACTOS (verde) : No chão",
            "• PÁSSAROS (marrom) : Voam alto",
            "",
            "Pressione qualquer tecla para voltar"
        ]
        
        # Fundo
        width, height = 700, 600
        x = GameConfig.SCREEN_WIDTH // 2 - width // 2
        y = GameConfig.SCREEN_HEIGHT // 2 - height // 2
        
        pygame.draw.rect(self.game.graphics_adapter.screen,
                        (0, 0, 0, 220),
                        (x, y, width, height),
                        border_radius=20)
        
        # Textos
        for i, line in enumerate(instructions):
            color = (255, 215, 0) if line.startswith("===") else (255, 255, 255)
            font_size = 48 if line.startswith("===") else 32
            font = pygame.font.Font(None, font_size)
            
            text_surf = font.render(line, True, color)
            text_rect = text_surf.get_rect(center=(GameConfig.SCREEN_WIDTH//2, 
                                                  y + 50 + i * 40))
            self.game.graphics_adapter.screen.blit(text_surf, text_rect)