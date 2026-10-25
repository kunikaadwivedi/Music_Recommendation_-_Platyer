from abc import ABC, abstractmethod
from typing import List
from entities.song import Song

class RecommendationStrategy(ABC):
    @abstractmethod
    def recommend(self, all_songs: List[Song]) -> List[Song]:
        pass