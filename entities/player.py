from entities.song import Song
from typing import List, Optional
from entities.user import User
from entities.playable import Playable
from state.stopped_state import StoppedState
from state.player_state import PlayerState

class Player:
    def __init__(self):
        self._state = StoppedState()
        self._queue: List[Song]= []
        self._current_index = -1
        self._current_user: Optional[User] = None
        
    def load(self, playable:Playable, user:User):
        self._current_user = user
        self._queue = playable.get_tracks()
        self._current_index = 0
        print(f"Loaded {len(self._queue)} tracks for user {user.get_name()}")
        self._state = StoppedState()
        
    def play_current_song_in_queue(self):
        if 0<= self._current_index < len(self._queue):
            song_to_play = self._queue[self._current_index]
            self._current_user.playback_strategy.play(song_to_play, self)
            
    def click_play(self):
        self._state.play(self)
        
    def click_pause(self):
        self._state.pause(self)
        
    def click_next(self):
        self._state.next(self)
        
    def advance_to_next_song(self):
        if self._current_index < len(self._queue) -1:
            self._current_index +=1
            self.play_current_song_in_queue()
            
        else:
            print("End of queue")
            self._state.stop(self)
    
    def change_state(self, state: 'PlayerState'):
        self._state = state
    
    def has_queue(self) -> bool:
        return len(self._queue) > 0