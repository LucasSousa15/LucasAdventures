
import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.adapters.asset_adapter import PygameAssetAdapter
from game.utils.config import GameConfig
from game.entities.player import Player
from game.entities.obstacle import Obstacle

def test_proportions():
    pygame.init()
    screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    adapter = PygameAssetAdapter()

    player = Player(GameConfig.SCREEN_WIDTH // 2, GameConfig.GROUND_LEVEL, adapter)
    cactus = Obstacle('cactus', adapter)
    bird = Obstacle('bird', adapter)

    cactus.x = 400
    cactus.y = cactus.get_initial_y()

    bird.x = 600
    bird.y = bird.get_initial_y()

    print("\n=== TESTE DE PROPORÇÕES ===")
    print(f"Tela: {GameConfig.SCREEN_WIDTH}x{GameConfig.SCREEN_HEIGHT}")
    print(f"Chão (Y): {GameConfig.GROUND_LEVEL}")
    print(f"\nJogador:")
    print(f"  Tamanho sprite: {player.image.get_width()}x{player.image.get_height()}")
    print(f"  Hitbox: {player.rect.width}x{player.rect.height}")
    print(f"  Posição: ({player.rect.x}, {player.rect.y})")
    print(f"\nCacto:")
    print(f"  Tamanho: {cactus.image.get_width()}x{cactus.image.get_height()}")
    print(f"  Posição: ({cactus.rect.x}, {cactus.rect.y})")
    print(f"\nPássaro:")
    print(f"  Tamanho: {bird.image.get_width()}x{bird.image.get_height()}")
    print(f"  Posição: ({bird.rect.x}, {bird.rect.y})")

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(GameConfig.SKY_BLUE)

        pygame.draw.line(screen, (255, 0, 0),
                        (0, GameConfig.GROUND_LEVEL),
                        (GameConfig.SCREEN_WIDTH, GameConfig.GROUND_LEVEL), 2)

        class SimpleGraphicsAdapter:
            def draw_sprite(self, img, x, y):
                screen.blit(img, (x, y))

        player.draw(SimpleGraphicsAdapter())
        cactus.draw(SimpleGraphicsAdapter())
        bird.draw(SimpleGraphicsAdapter())

        font = pygame.font.Font(None, 24)
        info = [
            "TESTE DE PROPORÇÕES",
            f"Jogador: {player.image.get_width()}x{player.image.get_height()}",
            f"Cacto: {cactus.image.get_width()}x{cactus.image.get_height()}",
            f"Pássaro: {bird.image.get_width()}x{bird.image.get_height()}",
            "",
            "Linha vermelha: nível do chão",
            "Pressione ESC para sair"
        ]

        for i, text in enumerate(info):
            text_surf = font.render(text, True, (255, 255, 255))
            screen.blit(text_surf, (10, 10 + i * 30))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    test_proportions()
