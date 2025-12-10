import pygame
from abc import ABC, abstractmethod

class GraphicsAdapter(ABC):


    @abstractmethod
    def init_display(self, width, height, title):
        pass

    @abstractmethod
    def clear(self, color):
        pass

    @abstractmethod
    def draw_sprite(self, sprite, x, y, flip=False):
        pass

    @abstractmethod
    def draw_rect(self, color, rect, width=0):
        pass

    @abstractmethod
    def draw_text(self, text, font, color, x, y):
        pass

    @abstractmethod
    def update_display(self):
        pass

class PygameGraphicsAdapter(GraphicsAdapter):


    def __init__(self):
        self.screen = None
        self.clock = pygame.time.Clock()

    def init_display(self, width, height, title):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        return self.screen

    def clear(self, color):
        if self.screen:
            self.screen.fill(color)

    def draw_sprite(self, sprite, x, y, flip=False):
        if sprite and self.screen:
            if flip:
                sprite = pygame.transform.flip(sprite, True, False)

            self.screen.blit(sprite, (int(x), int(y)))

    def draw_rect(self, color, rect, width=0):
        pygame.draw.rect(self.screen, color, rect, width)

    def draw_text(self, text, font, color, x, y):
        if isinstance(font, str):
            font_obj = pygame.font.Font(None, int(font))
        else:
            font_obj = font
        text_surface = font_obj.render(text, True, color)
        self.screen.blit(text_surface, (int(x), int(y)))

    def update_display(self):
        pygame.display.flip()
        self.clock.tick(60)

    def get_delta_time(self):
        return self.clock.get_time() / 1000.0
