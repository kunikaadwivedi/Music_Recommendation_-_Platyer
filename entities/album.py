from typing import List
from entities.song import Song
from entities.playable import Playable
from entities.artist import Artist

class Album(Playable): 
    def __init__(self, title:str, artist: 'Artist'):
        self._title = title
        self._artist = artist
        self._tracks: List[Song] = []
    
    def add_tracks(self, song: Song):
        self._tracks.append(song)
        
    def get_tracks(self) -> List[Song]:
        return self._tracks.copy()
    
    def get_title(self) -> str:
        return self._title
    
    def get_artist(self) -> 'Artist':
        return self._artist