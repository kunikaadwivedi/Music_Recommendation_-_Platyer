from __future__ import annotations
from state.player_state import PlayerState
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.player import Player

class PausedState(PlayerState):
    def play(self, player: Player):
        from state.playing_state import PlayingState
        print("Resuming playback.")
        player.change_state(PlayingState())
        
    def pause(self, player: Player):
        print("Already Paused.")
        
    def next(self, player: Player):
        from state.playing_state import PlayingState
        player.change_state(PlayingState())
        player.advance_to_next_song()
        
    def stop(self, player: Player):
        from state.stopped_state import StoppedState
        print("Stopping playback from paused state.")
        player.change_state(StoppedState())