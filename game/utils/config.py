import os

class GameConfig:
    # Tela Full HD (seu ajuste)
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    FPS = 60

    # Cores
    SKY_BLUE = (135, 206, 235)
    GROUND_COLOR = (86, 125, 70)

    @staticmethod
    def asset_path(*paths):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base_dir, "assets", *paths)

    # Jogador (seus valores)
    PLAYER_WIDTH = 233   # Largura do jogador
    PLAYER_HEIGHT = 397  # Altura do jogador
    PLAYER_SCALE = 0.5
    
    PLAYER_SPEED = 0
    JUMP_STRENGTH = -18  # Aumentado para tela maior
    GRAVITY = 0.8
    GROUND_LEVEL = 900   # Chão mais baixo na tela 1080p

    # Cenário
    CLOUD_COUNT = 8      # Mais nuvens para tela maior
    BACKGROUND_SCROLL_SPEED = 1.5  # Mais rápido para tela maior
    GROUND_SCROLL_SPEED = 6.0
    CLOUD_SPEED = 0.5

    # Obstáculos - TAMANHOS PROPORCIONAIS AO JOGADOR
    OBSTACLE_COUNT = 4   # Mais obstáculos
    OBSTACLE_SPAWN_RATE = 1800  # Mais frequente
    OBSTACLE_MIN_GAP = 400      # Maior gap para tela maior
    OBSTACLE_MAX_GAP = 800
    OBSTACLE_SPEED = 6.0        # Mais rápido

    # Fatores de proporção (para referência) - used to compute obstacle sizes
    PLAYER_TO_CACTUS_RATIO = 0.5    # Cacto = 50% do jogador
    PLAYER_TO_BIRD_RATIO = 0.35     # Pássaro = 35% do jogador

    # Debug helpers
    DEBUG_SHOW_COLLISIONS = True

    # Cactos - PROPORCIONAIS ao jogador (~50% da altura do jogador)
    CACTUS_COUNT = 3
    # Calculate cactus size proportional to player dimensions
    CACTUS_WIDTH = int(PLAYER_WIDTH * PLAYER_TO_CACTUS_RATIO)
    CACTUS_HEIGHT = int(PLAYER_HEIGHT * PLAYER_TO_CACTUS_RATIO)

    # Pássaros - PROPORCIONAIS ao jogador (~35% do tamanho do jogador)
    BIRD_COUNT = 2
    # Bird size proportional to player
    BIRD_WIDTH = int(PLAYER_WIDTH * PLAYER_TO_BIRD_RATIO)
    BIRD_HEIGHT = int(PLAYER_HEIGHT * PLAYER_TO_BIRD_RATIO)

    # Bird flight range: position birds low enough that player must jump to avoid them.
    # Range anchored to ground level and player height so it scales with screen/player size.
    BIRD_MIN_HEIGHT = int(GROUND_LEVEL - PLAYER_HEIGHT * 0.6)
    BIRD_MAX_HEIGHT = int(GROUND_LEVEL - PLAYER_HEIGHT * 0.25)

    # Pontuação
    SCORE_MULTIPLIER = 0.15  # Aumentado para tela maior
    HIGH_SCORE_FILE = "highscore.txt"

    # Jogo
    GAME_SPEED_INCREASE = 0.00015  # Aumentado
    INITIAL_GAME_SPEED = 1.0
    MAX_GAME_SPEED = 3.5           # Aumentado
    
    # (ratios already defined above)