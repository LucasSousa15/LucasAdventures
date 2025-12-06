
import os

class GameConfig:

    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    FPS = 60

    SKY_BLUE = (135, 206, 235)
    GROUND_COLOR = (86, 125, 70)

    @staticmethod
    def asset_path(*paths):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base_dir, "assets", *paths)

    GRAVITY = 1.0
    PLAYER_SPEED = 8
    JUMP_STRENGTH = -20
    GROUND_LEVEL = 1080 - 150  # Altura do chão

    CLOUD_COUNT = 10  # Mais nuvens para melhor cobertura
    BACKGROUND_SCROLL_SPEED = 0.05  # Parallax do fundo

    LEVEL_WIDTH = 10000  # Largura total do nível (ajustável)