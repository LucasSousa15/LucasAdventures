
from abc import ABC, abstractmethod

class GameState(ABC):
    
    
    def __init__(self, game):
        self.game = game
    
    @abstractmethod
    def handle_events(self):
        pass
    
    @abstractmethod
    def update(self, delta_time):
        pass
    
    @abstractmethod
    def render(self):
        pass
    
    def change_state(self, new_state):
        self.game.change_state(new_state)