from __future__ import annotations
from typing import TYPE_CHECKING
from strategy.playback.playback_strategy import PlaybackStrategy

if TYPE_CHECKING:
    from entities.song import Song
    from entities.player import Player

class PremiumPlaybackStrategy(PlaybackStrategy):
    def play(self, song: Song, player: Player):
        print(f"Premium User is now playing {song}")