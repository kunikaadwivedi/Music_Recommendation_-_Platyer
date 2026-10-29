# strategy/recommendation/two_stage_ranker_strategy.py
from typing import List, Dict, Tuple
from strategy.recommendation.recommendation_strategy import RecommendationStrategy
from strategy.recommendation.vector_recommendation_strategy import VectorRecommendationStrategy
from ml.ranking.gbdt_ranker import GBDTRanker
from entities.song import Song
from entities.user import User


class TwoStageRankerStrategy(RecommendationStrategy):
    """
    Stage 1: Vector Space Retrieval (TF-IDF Cosine Similarity) -> 30 Candidates
    Stage 2: GBDT Ranker (LightGBM personalization based on user profile) -> Top-K Output
    """
    def __init__(self):
        self.retrieval_engine = VectorRecommendationStrategy()
        self.ranker = GBDTRanker()

    def build_index(self, songs: List[Song]):
        self.retrieval_engine.build_index(songs)

    def recommend_for_user(
        self,
        user: User,
        seed_song: Song,
        all_songs: List[Song],
        top_k: int = 5
    ) -> List[Song]:
        if not self.retrieval_engine._is_indexed:
            self.retrieval_engine.build_index(all_songs)

        # Stage 1: Retrieve candidate pool (up to 30 items)
        query_tokens = self.retrieval_engine._tokenize(f"{seed_song.title} {seed_song.artist.get_name()}")
        from collections import Counter
        tf = Counter(query_tokens)
        query_vec = {}
        for t, c in tf.items():
            if t in self.retrieval_engine._idf:
                query_vec[t] = c * self.retrieval_engine._idf[t]

        norm = (sum(v**2 for v in query_vec.values()) ** 0.5) or 1.0
        query_vec = {t: v / norm for t, v in query_vec.items()}

        scored_candidates: List[Tuple[Song, float]] = []
        for idx, vec in enumerate(self.retrieval_engine._tfidf_vectors):
            candidate_song = self.retrieval_engine._song_map[idx]
            if candidate_song.id != seed_song.id:
                sim = self.retrieval_engine._cosine_similarity(query_vec, vec)
                scored_candidates.append((candidate_song, sim))

        # Sort by similarity and keep top 30
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        top_candidates = scored_candidates[:30]

        candidate_songs = [item[0] for item in top_candidates]
        candidate_sims = [item[1] for item in top_candidates]

        # Stage 2: GBDT Personalized Re-Ranking
        return self.ranker.rank(user, candidate_songs, candidate_sims, top_k=top_k)

    def recommend(self, all_songs: List[Song]) -> List[Song]:
        return all_songs[:5]