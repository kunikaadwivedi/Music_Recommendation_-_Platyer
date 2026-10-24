from strategy.recommendation.recommendation_strategy import RecommendationStrategy
from optional import List
from entities.song import Song

class RecommendationService:
    def __init__(self, strategy: RecommendationStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: RecommendationStrategy):
        self._strategy = strategy
    
    def generate_recommendations(self, all_songs: List[Song]) -> List[Song]:
        return self._strategy.recommend(all_songs)