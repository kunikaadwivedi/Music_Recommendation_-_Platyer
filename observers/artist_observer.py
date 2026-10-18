from abc import ABC, abstractmethod
from entities.artist import Artist
from entities.album import Album

class ArtistObserver(ABC):
    @abstractmethod
    def update(self, artist:'Artist', new_album: 'Album'):
        pass