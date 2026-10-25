from typing import List
from strategy.recommendation.recommendation_strategy import RecommendationStrategy
from entities.song import Song

class SimpleRecommendationStrategy(RecommendationStrategy):
    def recommend(self, all_songs: List[Song]) -> List[Song]:
        print("Generating Recommendation.....")
        return sorted(all_songs, key=lambda s: s.title)[:5]