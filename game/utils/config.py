
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
    GROUND_LEVEL = 1080 - 150

    CLOUD_COUNT = 10
    BACKGROUND_SCROLL_SPEED = 0.05

    LEVEL_WIDTH = 50000

    COIN_COUNT = 30  # Mais moedas
    COIN_ANIMATION_SPEED = 0.15
    COIN_VALUE = 10
    COIN_SPAWN_MIN_X = 100
    COIN_SPAWN_MAX_X = 4900
    COIN_SPAWN_MIN_Y = 400 
    COIN_SPAWN_MAX_Y = 700  
    COIN_SIZE = 100  # 
    COIN_HITBOX_SCALE = 0.7  