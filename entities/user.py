from enums.subscription_tier import SubscriptionTier
import uuid
from typing import Set

from entities.album import Album 
from entities.artist import Artist
from observers.artist_observer import ArtistObserver
from strategy.playback.playback_strategy import PlaybackStrategy
from strategy.playback.free_playback_strategy import FreePlaybackStrategy
from strategy.playback.premium_playback_strategy import PremiumPlaybackStrategy

class User(ArtistObserver):
    def __init__(self, name: str, tier: SubscriptionTier, songs_played: int):
        self._id = str(uuid.uuid4())
        self._name = name
        self._tier = tier
        if tier == SubscriptionTier.PREMIUM:
            self._playback_strategy = PremiumPlaybackStrategy()
        else:
            self._playback_strategy = FreePlaybackStrategy(songs_played)
        self._followed_artists: Set[Artist] = set()
        
    def follow_artist(self, artist: Artist):
        self._followed_artists.add(artist)
        artist.add_observer(self)
        
    def update(self, artist: Artist, new_album: Album):
        print(f"[Notification for {self._name}] Your followed artist {artist.get_name()} "
              f"just released a new album: {new_album.get_title()}")
        
    @property
    def playback_strategy(self) -> PlaybackStrategy:
        return self._playback_strategy
    
    @property
    def id(self) -> str:
        return self._id
    
    def get_name(self) -> str:
        return self._name