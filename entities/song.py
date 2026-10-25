from entities.playable import Playable
from entities.artist import Artist
from typing import List

class Song(Playable):
    def __init__(self, song_id: str, title: str, artist: 'Artist', duration_in_seconds: int):
        self._song_id = song_id
        self._title = title
        self._artist = artist
        self._duration_in_seconds = duration_in_seconds
        
    def get_tracks(self) -> List['Song']:
        return [self]
    
    def __str__(self) -> str:
        return f"'{self.title}' by {self._artist.get_name()}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def id(self) -> str:
        return self._song_id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def artist(self) -> 'Artist':
        return self._artist