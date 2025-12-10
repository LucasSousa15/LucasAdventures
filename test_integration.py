

import sys
import os
sys.path.insert(0, '.')

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from game.utils.config import GameConfig
from game.game import Game
import time

pygame.init()
game = Game()

print("=" * 80)
print("GAME INTEGRATION TEST - COLLISION VERIFICATION")
print("=" * 80)
print("\nStarting game... Testing for 10 seconds")
print("Monitoring: Bird spawn heights and collision events\n")

collision_count = 0
start_time = time.time()
max_bird_y = 0
min_bird_y = 1000

try:
    while time.time() - start_time < 10:

        state = game.state

        if hasattr(state, 'game_manager'):

            for obs in state.game_manager.obstacles:
                if obs.type == "bird":
                    max_bird_y = max(max_bird_y, obs.y)
                    min_bird_y = min(min_bird_y, obs.y)

        game.update(0.016)

except KeyboardInterrupt:
    pass
except Exception as e:
    print(f"\nError during test: {e}")

end_time = time.time()
duration = end_time - start_time

print(f"\nTest completed in {duration:.1f} seconds")
print(f"\nResults:")
print(f"  Game Speed: {game.state.game_manager.game_speed:.2f}")
print(f"  Player Y: {game.state.player.rect.midbottom[1]:.0f}px")
print(f"  Bird Y range spawned: {min_bird_y}-{max_bird_y}px")
print(f"  Expected safe range: 562-761px")

if min_bird_y >= 562 and max_bird_y <= 761:
    print(f"\n[OK] All birds spawned in safe range!")
else:
    print(f"\n[WARNING] Some birds outside safe range!")
    if min_bird_y < 562:
        print(f"  Min: {min_bird_y} < 562")
    if max_bird_y > 761:
        print(f"  Max: {max_bird_y} > 761")

print("\n" + "=" * 80)
pygame.quit()
