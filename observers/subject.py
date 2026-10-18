from observers.artist_observer import ArtistObserver
from typing import List
from entities.artist import Artist
from entities.album import Album

class Subject:
    def __init__(self):
        self._observers: List[ArtistObserver] = []
    
    def add_observer(self,observer: ArtistObserver):
        if observer in self._observers:
            return f'Already exist'
        self._observers.append(observer)
    
    def remove_observer(self,observer: ArtistObserver):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observer(self, artist: 'Artist', album: 'Album'):
        for observer in self._observers:
            observer.update(artist, album)
            