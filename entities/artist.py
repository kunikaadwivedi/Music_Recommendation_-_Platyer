from observers.subject import Subject
from entities.album import Album
from typing import List

class Artist(Subject):
    def __init__(self, artist_id: str, name: str):
        self._artist_id = artist_id
        self._name = name
        self.discography: List['Album'] = []
        
    def release_album(self, album: 'Album'):
        self._discography.append(album)
        print(f"[System] Artist {self._name} has released a new album: {album.get_title()}")
        self.notify_observers(self, album)
    
    @property
    def id(self) -> str:
        return self._id
    
    def get_name(self) -> str:
        return self._name