from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.song import Song
    from entities.player import Player

class PlaybackStrategy(ABC):
    @abstractmethod
    def play(self, song: Song, player: Player):
        pass