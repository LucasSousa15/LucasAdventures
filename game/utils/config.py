# game/utils/config.py
import os

class GameConfig:
    # Configurações de tela
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    FPS = 60
    
    # Cores
    SKY_BLUE = (135, 206, 235)
    GROUND_GREEN = (50, 200, 50)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    # Caminhos
    @staticmethod
    def asset_path(*paths):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base_dir, "assets", *paths)
    
    # Física
    GRAVITY = 1.0
    PLAYER_SPEED = 8
    JUMP_STRENGTH = -20
    GROUND_LEVEL = 1080 - 100