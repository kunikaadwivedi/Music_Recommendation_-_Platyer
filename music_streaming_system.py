import threading
from typing import Dict, List
from entities.song import Song
from entities.artist import Artist
from entities.user import User
from entities.player import Player
from strategy.recommendation.simple_recommendation_strategy import SimpleRecommendationStrategy
from services.search_service import SearchService
from services.recommendation_service import RecommendationService

class MusicStreamingSystem:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._users: Dict[str, User] = {}
            self._songs: Dict[str, Song] = {}
            self._artists: Dict[str, Artist] = {}
            self._player = Player()
            self._search_service = SearchService()
            self._recommendation_service = RecommendationService(SimpleRecommendationStrategy())
            self._initialized = True
    
    def ingest_from_spotify(self, query: str = "year:2024", limit: int = 10) -> int:
        """Pulls live streaming tracks via Spotify Search API and maps into domain entities."""
        from services.spotify_client import SpotifyClient
        client = SpotifyClient()
        raw_tracks = client.search_tracks(query=query, limit=limit)
        
        count = 0
        for item in raw_tracks:
            if not item.get("id"):
                continue
            artist_data = item["artists"][0]
            artist_id = artist_data["id"]
            artist_name = artist_data["name"]

            # Register or retrieve artist
            if artist_id not in self._artists:
                self.add_artist(Artist(artist_id, artist_name))

            song_id = item["id"]
            title = item["name"]
            duration = int(item.get("duration_ms", 180000) / 1000)
            spotify_url = item.get("external_urls", {}).get("spotify")
            preview_url = item.get("preview_url")

            song = Song(
                song_id=song_id,
                title=title,
                artist=self._artists[artist_id],
                duration_in_seconds=duration,
                spotify_url=spotify_url,
                preview_url=preview_url
            )
            self._songs[song.id] = song
            count += 1

        print(f"[System] Ingested {count} live tracks from Spotify for query '{query}'.")
        return count

    def get_vector_recommendations(self, seed_song: Song, top_k: int = 5) -> List[Song]:
        """Runs vector-based similarity search using the active strategy."""
        from strategy.recommendation.vector_recommendation_strategy import VectorRecommendationStrategy
        if isinstance(self._recommendation_service._strategy, VectorRecommendationStrategy):
            return self._recommendation_service._strategy.recommend_similar(
                seed_song, list(self._songs.values()), top_k=top_k
            )
        return self._recommendation_service.generate_recommendations(list(self._songs.values()))
            
    @classmethod
    def get_instance(cls):
        return cls()
    
    def register_user(self, user: User):
        self._users[user.id] = user
        
    def add_song(self, song_id: str, title: str, artist_id: str, duration: int) -> Song:
        song = Song(song_id, title, self._artists[artist_id], duration)
        self._songs[song.id] = song
        return song
    
    def add_artist(self, artist: Artist):
        self._artists[artist.id] = artist
    
    def search_songs_by_title(self, title: str) -> List[Song]:
        return self._search_service.search_songs_by_title(list(self._songs.values()), title)
    
    def search_artists_by_name(self, name: str) -> List[Artist]:
        return self._search_service.search_artists_by_name(list(self._artists.values()), name)
    
    def get_song_recommendations(self) -> List[Song]:
        return self._recommendation_service.generate_recommendations(list(self._songs.values()))
    
    def get_player(self) -> Player:
        return self._player