from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.player import Player

class PlayerState(ABC):
    @abstractmethod
    def play(self, player: Player):
        pass
    
    @abstractmethod
    def pause(self, player: Player):
        pass

    @abstractmethod
    def next(self, player: Player):
        pass
    
    @abstractmethod
    def stop(self, player: Player):
        pass