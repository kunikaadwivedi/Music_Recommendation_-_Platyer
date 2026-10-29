# entities/song.py
from __future__ import annotations
from typing import List, Optional, Dict
from entities.playable import Playable
from entities.artist import Artist

class Song(Playable):
    def __init__(
        self,
        song_id: str,
        title: str,
        artist: Artist,
        duration_in_seconds: int,
        genres: Optional[List[str]] = None,
        audio_features: Optional[Dict[str, float]] = None,
        spotify_url: Optional[str] = None,
        preview_url: Optional[str] = None
    ):
        self._song_id = song_id
        self._title = title
        self._artist = artist
        self._duration_in_seconds = duration_in_seconds
        self._genres = genres or []
        self._audio_features = audio_features or {}
        self._spotify_url = spotify_url
        self._preview_url = preview_url
        self._embedding: Optional[List[float]] = None  # Ready for vector search

    def get_tracks(self) -> List[Song]:
        return [self]

    @property
    def id(self) -> str:
        return self._song_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def artist(self) -> Artist:
        return self._artist

    @property
    def duration_in_seconds(self) -> int:
        return self._duration_in_seconds

    @property
    def audio_features(self) -> Dict[str, float]:
        return self._audio_features

    @property
    def spotify_url(self) -> Optional[str]:
        return self._spotify_url

    @property
    def preview_url(self) -> Optional[str]:
        return self._preview_url

    @property
    def embedding(self) -> Optional[List[float]]:
        return self._embedding

    @embedding.setter
    def embedding(self, vector: List[float]):
        self._embedding = vector

    def __str__(self) -> str:
        return f"'{self._title}' by {self._artist.get_name()}"

    def __repr__(self) -> str:
        return self.__str__()