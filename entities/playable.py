from abc import ABC, abstractmethod
from typing import List
from entities.song import Song

class Playable(ABC):
    @abstractmethod
    def get_tracks(self) -> List['Song']:
        pass