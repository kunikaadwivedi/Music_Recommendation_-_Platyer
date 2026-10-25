from __future__ import annotations
from state.player_state import PlayerState
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.player import Player

class StoppedState(PlayerState):
    def play(self, player: Player):
        if player.has_queue():
            from state.playing_state import PlayingState
            print("Starting playback.")
            player.change_state(PlayingState())
            player.play_current_song_in_queue()
        else:
            print("Queue is empty. Load songs to play.")
            
    def pause(self, player: Player):
        print("Cannot pause. Player is stopped.")
        
    def next(self, player: Player):
        print("Cannot skip. Player is stopped.")
        
    def stop(self, player: Player):
        print("Already stopped.")