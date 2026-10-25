from __future__ import annotations
from typing import TYPE_CHECKING
from strategy.playback.playback_strategy import PlaybackStrategy

if TYPE_CHECKING:
    from entities.player import Player
    from entities.song import Song

class FreePlaybackStrategy(PlaybackStrategy):
    SONGS_BEFORE_AD = 3
    
    def __init__(self, initial_songs_played: int):
        self._songs_played = initial_songs_played    

    def play(self, song: Song, player: Player):
        if self._songs_played > 0 and self._songs_played % self.SONGS_BEFORE_AD == 0:
            print("\n>>> Playing Advertisement: 'Buy Spotify Premium for ad-free music!' <<<\n")
        print(f"Free User is now playing: {song}")
        self._songs_played += 1