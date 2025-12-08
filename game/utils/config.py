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

    # Cactos - PROPORCIONAIS ao jogador (~50% da altura do jogador)
    CACTUS_COUNT = 3
    CACTUS_WIDTH = 120   # AUMENTADO: ~50% da largura do jogador
    CACTUS_HEIGHT = 200  # AUMENTADO: ~50% da altura do jogador

    # Pássaros - PROPORCIONAIS ao jogador (~35% do tamanho do jogador)
    BIRD_COUNT = 2
    BIRD_WIDTH = 80      # NOVO: largura específica
    BIRD_HEIGHT = 80     # NOVO: altura específica
    
    # Alturas ajustadas para tela 1080p
    BIRD_MIN_HEIGHT = 400  # MAIS ALTO: para tela maior
    BIRD_MAX_HEIGHT = 650  # MAIS ALTO: para tela maior

    # Pontuação
    SCORE_MULTIPLIER = 0.15  # Aumentado para tela maior
    HIGH_SCORE_FILE = "highscore.txt"

    # Jogo
    GAME_SPEED_INCREASE = 0.00015  # Aumentado
    INITIAL_GAME_SPEED = 1.0
    MAX_GAME_SPEED = 3.5           # Aumentado
    
    # Fatores de proporção (para referência)
    PLAYER_TO_CACTUS_RATIO = 0.5    # Cacto = 50% do jogador
    PLAYER_TO_BIRD_RATIO = 0.35     # Pássaro = 35% do jogador