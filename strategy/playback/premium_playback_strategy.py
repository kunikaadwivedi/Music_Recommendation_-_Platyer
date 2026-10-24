from strategy.playback.playback_strategy import PlaybackStrategy
from entities.song import Song
from entities.player import Player

class PremiumPlaybackStrategy(PlaybackStrategy):
    def play(self, song:Song, player:Player):
        print(f"Premium User is now playing {song}")