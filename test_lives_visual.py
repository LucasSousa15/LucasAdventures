
"""
Visual test for lives system - Run game for 5 seconds and take damage
"""
import sys
import os
sys.path.insert(0, '.')

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
from game.utils.config import GameConfig
from game.game import Game
import time


pygame.init()
game = Game()

print("=" * 80)
print("LIVES SYSTEM VISUAL TEST")
print("=" * 80)
print("\nRunning game for 10 seconds...")
print("Watch for:")
print("  - Lives counter in top-left corner")
print("  - Collisions reducing lives")
print("  - Game over when lives reach 0\n")


start_time = time.time()
last_lives = 3
collision_count = 0

try:
    while time.time() - start_time < 10:
        current_lives = game.state.game_manager.lives


        if current_lives < last_lives:
            collision_count += 1
            print(f"[COLLISION] Lives reduced: {last_lives} -> {current_lives}")
            last_lives = current_lives


        game.update(0.016)


        if game.state.game_manager.is_game_over:
            print(f"\n[GAME OVER] Final score: {game.state.game_manager.score:.0f}")
            print(f"[GAME OVER] Lives when ended: {game.state.game_manager.lives}")
            break

except KeyboardInterrupt:
    pass

end_time = time.time()
duration = end_time - start_time

print(f"\nTest Results:")
print(f"  Duration: {duration:.1f}s")
print(f"  Collisions: {collision_count}")
print(f"  Current lives: {game.state.game_manager.lives}")
print(f"  Game over: {game.state.game_manager.is_game_over}")

print("\n" + "=" * 80)
pygame.quit()
