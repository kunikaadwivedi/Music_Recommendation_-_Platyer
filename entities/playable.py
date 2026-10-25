from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.song import Song

class Playable(ABC):
    @abstractmethod
    def get_tracks(self) -> List[Song]:
        pass