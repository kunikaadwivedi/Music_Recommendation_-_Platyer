from abc import ABC, abstractmethod
from entities.player import Player

class PlayerState(ABC):
    @abstractmethod
    def play(self, player: 'Player'):
        pass
    
    @abstractmethod
    def pause(self, player: 'Player'):
        pass
    
    @abstractmethod
    def stop(self, player:'Player'):
        pass