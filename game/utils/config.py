import os

class GameConfig:
    # Configurações de tela
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    FPS = 60
    
    # Cores (fallback caso assets não carreguem)
    SKY_BLUE = (135, 206, 235)
    GROUND_COLOR = (86, 125, 70)
    
    # Caminhos
    @staticmethod
    def asset_path(*paths):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base_dir, "assets", *paths)
    
    # Física
    GRAVITY = 1.0
    PLAYER_SPEED = 8
    JUMP_STRENGTH = -20
    GROUND_LEVEL = 1080 - 150  # Ajustado para considerar o chão gráfico
    
    # Cenário
    CLOUD_COUNT = 5  # Número de nuvens
    CLOUD_SPEED = 0.5  # Velocidade base das nuvens
    BACKGROUND_SCROLL_SPEED = 0.1  # Velocidade do parallax do fundo