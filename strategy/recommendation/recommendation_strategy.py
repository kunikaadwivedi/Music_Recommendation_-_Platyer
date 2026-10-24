from abc import ABC, abstractmethod
from optional import List
from entities.song import Song

class RecommendationSystem(ABC):
    @abstractmethod
    def recommend(self, all_songs:List[Song]) -> List[Song]:
        pass
    
