

import sys
import random

sys.path.insert(0, '.')

from game.utils.config import GameConfig
from game.entities.obstacle import Obstacle
from game.adapters.asset_adapter import PygameAssetAdapter

print("=" * 80)
print("BIRD HEIGHT POSITIONING TEST")
print("=" * 80)

print(f"\n1. CONFIGURATION VALUES:")
print(f"   PLAYER_HEIGHT: {GameConfig.PLAYER_HEIGHT}px")
print(f"   GROUND_LEVEL: {GameConfig.GROUND_LEVEL}px")
print(f"   PLAYER_TO_BIRD_RATIO: {GameConfig.PLAYER_TO_BIRD_RATIO}")

bird_h = int(GameConfig.PLAYER_HEIGHT * GameConfig.PLAYER_TO_BIRD_RATIO)
print(f"   BIRD_HEIGHT: {bird_h}px (calculated from ratio)")

print(f"\n2. BIRD HEIGHT LIMITS:")
print(f"   BIRD_MIN_HEIGHT: {GameConfig.BIRD_MIN_HEIGHT}px")
print(f"   BIRD_MAX_HEIGHT: {GameConfig.BIRD_MAX_HEIGHT}px")
print(f"   Safe spawn Y-range for bird.midbottom: {GameConfig.BIRD_MIN_HEIGHT} to {GameConfig.BIRD_MAX_HEIGHT}")

print(f"\n3. BIRD TOP POSITION (visual top Y):")
min_top = GameConfig.BIRD_MIN_HEIGHT - bird_h
max_top = GameConfig.BIRD_MAX_HEIGHT - bird_h
print(f"   If bird.midbottom.y at MIN ({GameConfig.BIRD_MIN_HEIGHT}): bird.top = {min_top}px")
print(f"   If bird.midbottom.y at MAX ({GameConfig.BIRD_MAX_HEIGHT}): bird.top = {max_top}px")
print(f"   Bird visual range (top): {min_top} to {max_top}")

print(f"\n4. PLAYER HITBOX POSITION:")
player_hitbox_h = int(GameConfig.PLAYER_HEIGHT * 0.7)
player_bottom = GameConfig.GROUND_LEVEL
player_top = player_bottom - player_hitbox_h
print(f"   PLAYER_HITBOX_HEIGHT: {player_hitbox_h}px")
print(f"   Player at ground (midbottom Y={player_bottom}): top={player_top}, bottom={player_bottom}")

print(f"\n5. COLLISION ANALYSIS:")
print(f"   Player Y range: {player_top} to {player_bottom}")
print(f"   Bird Y range (visual): {min_top} to {max_top}")
if max_top < player_top:
    print(f"   ✓ SAFE: All birds spawn ABOVE player (max_bird_top={max_top} < player_top={player_top})")
else:
    print(f"   ✗ DANGER: Some birds may overlap with player (max_bird_top={max_top} >= player_top={player_top})")

print(f"\n6. SECONDARY SAFETY CHECK (in get_initial_y):")
safety_min = max(
    GameConfig.BIRD_MIN_HEIGHT,
    GameConfig.GROUND_LEVEL - (GameConfig.PLAYER_HEIGHT * 0.9)
)
print(f"   safety_min = max({GameConfig.BIRD_MIN_HEIGHT}, {GameConfig.GROUND_LEVEL} - {GameConfig.PLAYER_HEIGHT * 0.9})")
print(f"   safety_min = max({GameConfig.BIRD_MIN_HEIGHT}, {GameConfig.GROUND_LEVEL - GameConfig.PLAYER_HEIGHT * 0.9})")
print(f"   safety_min = {safety_min}px")
print(f"   Actual spawn range: {safety_min} to {GameConfig.BIRD_MAX_HEIGHT}")

print(f"\n7. TESTING get_initial_y() WITH 20 RANDOM CALLS:")
asset_adapter = PygameAssetAdapter()
random_heights = []
for i in range(20):
    bird = Obstacle("bird", asset_adapter)
    height = bird.get_initial_y()
    random_heights.append(height)
    print(f"   Call {i+1:2d}: Y={height:4d}px (bird.top would be at {height - bird_h}px)")

min_spawn = min(random_heights)
max_spawn = max(random_heights)
print(f"\n   Spawned range: {min_spawn} to {max_spawn}")
print(f"   Expected range: {safety_min} to {GameConfig.BIRD_MAX_HEIGHT}")

if min_spawn >= safety_min and max_spawn <= GameConfig.BIRD_MAX_HEIGHT:
    print(f"   ✓ All spawns within safe range")
else:
    print(f"   ✗ WARNING: Some spawns outside range!")
    if min_spawn < safety_min:
        print(f"      Min spawn {min_spawn} < safety_min {safety_min}")
    if max_spawn > GameConfig.BIRD_MAX_HEIGHT:
        print(f"      Max spawn {max_spawn} > BIRD_MAX_HEIGHT {GameConfig.BIRD_MAX_HEIGHT}")

print("\n" + "=" * 80)
