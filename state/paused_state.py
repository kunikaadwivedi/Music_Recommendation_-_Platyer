from state.player_state import PlayerState
from entities.player import Player
from state.playing_state import PlayingState
from state.stopped_state import StoppedState

class PausedState(PlayerState):
    def play(self, player:Player):
        print("Resuming playback.")
        player.change_state(PlayingState())
        
    def pause(self, player:Player):
        print("Already Paused.")
        
    def next(self, player:Player):
        player.change_state(PlayingState())
        player.advance_to_next_song()
        
    def stop(self, player:Player):
        print("Stopping playback from paused state.")
        player.change_state(StoppedState())