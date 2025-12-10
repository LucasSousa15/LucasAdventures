

import sys
sys.path.insert(0, '.')

from game.utils.config import GameConfig
from game.entities.game_manager import GameManager
from game.entities.player import Player
from game.adapters.asset_adapter import PygameAssetAdapter
import pygame

pygame.init()
pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))

print("=" * 80)
print("GAME MANAGER BIRD SPAWN TEST")
print("=" * 80)

asset_adapter = PygameAssetAdapter()
game_manager = GameManager(asset_adapter)

print(f"\n1. SPAWNING 20 OBSTACLES:")
for i in range(20):
    player_rect = pygame.Rect(0, 0, 139, 277)
    game_manager.spawn_obstacle(player_rect)

    last_obstacle = game_manager.obstacles[-1]
    if last_obstacle.type == "bird":
        print(f"   Bird {i}: Y={last_obstacle.y:4d}px, " +
              f"rect.midbottom.y={last_obstacle.rect.midbottom[1]:4d}px, " +
              f"coll_rect.midbottom.y={last_obstacle.collision_rect.midbottom[1]:4d}px")

        if last_obstacle.y != last_obstacle.rect.midbottom[1]:
            print(f"      ERROR: Y mismatch! y={last_obstacle.y} != rect.y={last_obstacle.rect.midbottom[1]}")
        if last_obstacle.rect.midbottom[1] != last_obstacle.collision_rect.midbottom[1]:
            print(f"      ERROR: Collision rect mismatch!")

bird_obstacles = [obs for obs in game_manager.obstacles if obs.type == "bird"]
print(f"\n2. STATISTICS:")
print(f"   Total obstacles spawned: {len(game_manager.obstacles)}")
print(f"   Birds: {len(bird_obstacles)}")
print(f"   Cactus: {len(game_manager.obstacles) - len(bird_obstacles)}")

if bird_obstacles:
    y_values = [bird.y for bird in bird_obstacles]
    print(f"\n3. BIRD Y-POSITIONS:")
    print(f"   Min: {min(y_values)}px (expected: >=562)")
    print(f"   Max: {max(y_values)}px (expected: <=761)")
    print(f"   Expected range: 562-761")

    in_range = sum(1 for y in y_values if 562 <= y <= 761)
    print(f"   Birds in safe range: {in_range}/{len(bird_obstacles)}")

    if min(y_values) >= 562 and max(y_values) <= 761:
        print(f"   [OK] All birds within safe spawn range!")
    else:
        print(f"   [WARNING] Some birds outside safe range!")

print("\n" + "=" * 80)
pygame.quit()
