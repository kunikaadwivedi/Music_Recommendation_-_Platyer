from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.artist import Artist
    from entities.album import Album

class ArtistObserver(ABC):
    @abstractmethod
    def update(self, artist: Artist, new_album: Album):
        pass