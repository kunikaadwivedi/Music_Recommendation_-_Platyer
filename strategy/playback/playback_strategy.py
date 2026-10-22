from abc import ABC, abstractmethod
from entities.song import Song
from entities.player import Player

class PlaybackStrategy(ABC):
    @abstractmethod
    def play(self, song:Song,player:Player):
        pass