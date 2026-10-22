from state.player_state import PlayerState
from entities.player import Player
from state.paused_state import PausedState
from state.stopped_state import StoppedState

class PlayingState(PlayerState):
    def play(self, player: 'Player'):
        print('Already Playing.')
        
    def next(self, player: 'Player'):
        player.advance_to_next_song()
        
    def pause(self, player: 'Player'):
        print("Pausing playback.")
        player.change_state(PausedState())
        
    def stop(self, player: 'Player'):
        print("Stopping playback.")
        player.change_state(StoppedState())
        
    