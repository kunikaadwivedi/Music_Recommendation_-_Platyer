from __future__ import annotations
from state.player_state import PlayerState
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.player import Player

class PlayingState(PlayerState):
    def play(self, player: Player):
        print('Already Playing.')
        
    def next(self, player: Player):
        player.advance_to_next_song()
        
    def pause(self, player: Player):
        from state.paused_state import PausedState
        print("Pausing playback.")
        player.change_state(PausedState())
        
    def stop(self, player: Player):
        from state.stopped_state import StoppedState
        print("Stopping playback.")
        player.change_state(StoppedState())