from __future__ import annotations
from typing import List, TYPE_CHECKING
from entities.playable import Playable
from entities.song import Song

if TYPE_CHECKING:
    from entities.artist import Artist

class Album(Playable): 
    def __init__(self, title: str, artist: Artist):
        self._title = title
        self._artist = artist
        self._tracks: List[Song] = []
    
    def add_track(self, song: Song):
        self._tracks.append(song)
        
    def get_tracks(self) -> List[Song]:
        return self._tracks.copy()
    
    def get_title(self) -> str:
        return self._title
    
    def get_artist(self) -> Artist:
        return self._artist