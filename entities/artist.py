from __future__ import annotations
from typing import List, TYPE_CHECKING
from observers.subject import Subject

if TYPE_CHECKING:
    from entities.album import Album

class Artist(Subject):
    def __init__(self, artist_id: str, name: str):
        super().__init__()
        self._artist_id = artist_id
        self._name = name
        self._discography: List[Album] = []
        
    def release_album(self, album: Album):
        self._discography.append(album)
        print(f"[System] Artist {self._name} has released a new album: {album.get_title()}")
        self.notify_observer(self, album)
    
    @property
    def id(self) -> str:
        return self._artist_id
    
    def get_name(self) -> str:
        return self._name