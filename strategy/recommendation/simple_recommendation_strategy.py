from recommendation.recommendation_strategy import RecommendationSystem
from optional import List
from entities.song import Song

class SimpleRecommendationSystem(RecommendationSystem):
    def recommend(self, all_songs: List[Song]) -> List[Song]:
        print("Generating Recommendation.....")
        return sorted(all_songs, key = lambda s: s.title)[:5]