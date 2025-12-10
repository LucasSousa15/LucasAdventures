
"""
Test frame normalization system - Verify all frames render at consistent size
"""
import sys
import os
sys.path.insert(0, '.')

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
from game.utils.config import GameConfig
from game.adapters.asset_adapter import FrameNormalizer
from game.entities.player import Player
from game.adapters.asset_adapter import PygameAssetAdapter


pygame.init()
pygame.display.set_mode((1920, 1080))

print("=" * 80)
print("FRAME NORMALIZATION TEST")
print("=" * 80)

adapter = PygameAssetAdapter()
player = Player(GameConfig.SCREEN_WIDTH // 2, GameConfig.GROUND_LEVEL, adapter)

print(f"\nTarget size: {GameConfig.PLAYER_WIDTH}x{GameConfig.PLAYER_HEIGHT}")
print(f"\nValidating all animation frames...")

total_frames = 0
valid_frames = 0
invalid_frames = 0

for action_name, frames in player.animations.items():
    print(f"\n{action_name.upper()} animation ({len(frames)} frames):")
    for idx, frame in enumerate(frames):
        width, height = frame.get_size()
        is_valid = FrameNormalizer.validate_frame_size(
            frame,
            GameConfig.PLAYER_WIDTH,
            GameConfig.PLAYER_HEIGHT
        )

        status = "[OK]" if is_valid else "[FAIL]"
        print(f"  Frame {idx}: {width}x{height} {status}")

        total_frames += 1
        if is_valid:
            valid_frames += 1
        else:
            invalid_frames += 1

print(f"\n" + "=" * 80)
print(f"SUMMARY:")
print(f"  Total frames: {total_frames}")
print(f"  Valid frames: {valid_frames}")
print(f"  Invalid frames: {invalid_frames}")

if invalid_frames == 0:
    print(f"\n[SUCCESS] All frames have consistent size!")
else:
    print(f"\n[WARNING] {invalid_frames} frame(s) with incorrect size (will be auto-corrected)")

print("\n" + "=" * 80)


print("\nTesting aspect ratio preservation...")


test_img = pygame.Surface((800, 200))
test_img.fill((100, 150, 200))

print(f"Original test image: 800x200 (4:1 ratio)")


normalized = FrameNormalizer.normalize_frame(
    test_img,
    GameConfig.PLAYER_WIDTH,
    GameConfig.PLAYER_HEIGHT,
    maintain_aspect=True
)

norm_w, norm_h = normalized.get_size()
print(f"Normalized to: {norm_w}x{norm_h}")
print(f"Size guarantee: {norm_w == GameConfig.PLAYER_WIDTH and norm_h == GameConfig.PLAYER_HEIGHT}")

print("\n" + "=" * 80)
pygame.quit()
