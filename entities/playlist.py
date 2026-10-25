from typing import List
from entities.song import Song
from entities.playable import Playable

class Playlist(Playable): 
    def __init__(self, name: str):
        self._name = name
        self._tracks: List[Song] = []
    
    def add_track(self, song: Song):
        self._tracks.append(song)
        
    def get_tracks(self) -> List[Song]:
        return self._tracks.copy()