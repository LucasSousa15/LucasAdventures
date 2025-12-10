import pygame
import os
from abc import ABC, abstractmethod

class FrameNormalizer:


    @staticmethod
    def normalize_frame(surface, target_width, target_height, maintain_aspect=True, align_bottom=False):

        if surface is None:
            return FrameNormalizer._create_placeholder(target_width, target_height)

        if maintain_aspect:

            original_width, original_height = surface.get_size()

            scale_w = target_width / original_width
            scale_h = target_height / original_height
            scale = min(scale_w, scale_h)

            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

            if (new_width, new_height) != (original_width, original_height):
                scaled = pygame.transform.scale(surface, (new_width, new_height))
            else:
                scaled = surface

            result = pygame.Surface((target_width, target_height), pygame.SRCALPHA)
            result.fill((0, 0, 0, 0))

            offset_x = (target_width - new_width) // 2

            if align_bottom:
                offset_y = target_height - new_height
            else:
                offset_y = (target_height - new_height) // 2
            result.blit(scaled, (offset_x, offset_y))

            return result
        else:

            return pygame.transform.scale(surface, (target_width, target_height))

    @staticmethod
    def validate_frame_size(surface, expected_width, expected_height):

        if surface is None:
            return False

        actual_w, actual_h = surface.get_size()
        return actual_w == expected_width and actual_h == expected_height

    @staticmethod
    def _create_placeholder(width, height):

        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((50, 50, 50, 200))
        pygame.draw.rect(surface, (255, 100, 100, 255), surface.get_rect(), 2)
        return surface


class AssetAdapter(ABC):


    @abstractmethod
    def load_image(self, path, use_alpha=True):
        pass

    @abstractmethod
    def load_animation_frames(self, folder, animation_name, frame_count):
        pass

class PygameAssetAdapter(AssetAdapter):


    def load_image(self, path, use_alpha=True):
        try:
            if use_alpha:
                image = pygame.image.load(path).convert_alpha()
            else:
                image = pygame.image.load(path).convert()
            return image
        except pygame.error as e:
            print(f"Erro ao carregar imagem {path}: {e}")
            return self._create_fallback_surface(800, 600, (100, 100, 255))
        except Exception as e:
            print(f"Erro inesperado ao carregar {path}: {e}")
            return self._create_fallback_surface(800, 600, (255, 100, 100))

    def load_animation_frames(self, folder, animation_name, frame_count):
        frames = []
        for i in range(frame_count):
            frame_path = os.path.join(folder, f"{animation_name}_{i}.png")
            frames.append(self.load_image(frame_path))
        return frames

    def get_obstacle_asset(self, obstacle_type, frame_index):

        folder = self._resolve_obstacle_folder(obstacle_type)
        if folder is None:
            print(f"[ERRO] Pasta de obstáculo '{obstacle_type}' não encontrada.")
            return None

        path = os.path.join(folder, f"{frame_index}.png")

        if not os.path.exists(path):
            return None

        try:
            return pygame.image.load(path).convert_alpha()
        except Exception as e:
            print(f"[ERRO] Falha ao carregar frame '{path}': {e}")
            return None

    def _resolve_obstacle_folder(self, obstacle_type):
        base_assets = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "assets"
        )

        folder = os.path.join(base_assets, obstacle_type)

        if os.path.isdir(folder):
            return folder

        return None

    def _create_fallback_surface(self, width=64, height=64, color=(255, 0, 255)):
        surf = pygame.Surface((width, height))
        surf.fill(color)
        return surf
