import pygame
from abc import ABC, abstractmethod

class InputAdapter(ABC):
    """Interface para diferentes esquemas de controle"""
    
    @abstractmethod
    def get_movement(self):
        """Retorna (dx, dy, jump_pressed)"""
        pass
    
    @abstractmethod
    def get_menu_input(self):
        """Retorna entrada para menus"""
        pass
    
    @abstractmethod
    def should_quit(self):
        """Retorna True se o jogo deve fechar"""
        pass

class KeyboardInputAdapter(InputAdapter):
    """Adapter para controle por teclado"""
    
    def __init__(self, config=None):
        self.config = config or {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'jump': pygame.K_SPACE,
            'pause': pygame.K_ESCAPE,
            'action': pygame.K_LCTRL
        }
    
    def get_movement(self):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[self.config['left']]:
            dx = -1
        if keys[self.config['right']]:
            dx = 1
        
        jump_pressed = keys[self.config['jump']]
        
        return dx, 0, jump_pressed
    
    def get_menu_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 'select'
                elif event.key == pygame.K_UP:
                    return 'up'
                elif event.key == pygame.K_DOWN:
                    return 'down'
                elif event.key == pygame.K_ESCAPE:
                    return 'back'
        return None
    
    def should_quit(self):
        for event in pygame.event.get(pygame.QUIT):
            return True
        return False