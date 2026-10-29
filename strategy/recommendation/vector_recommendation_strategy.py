from typing import List, Dict, Optional
import math
import re
from collections import Counter
from strategy.recommendation.recommendation_strategy import RecommendationStrategy
from entities.song import Song


class VectorRecommendationStrategy(RecommendationStrategy):
    """
    Two-Stage Information Retrieval Engine:
    Stage 1: Term Frequency-Inverse Document Frequency (TF-IDF) Vector Retrieval
             with Cosine Similarity over track metadata (title, artist).
    Stage 2: Maximal Marginal Relevance (MMR) Re-Ranking for catalog diversity.
    """
    def __init__(self):
        print("[AI Engine] Initializing Dense TF-IDF Vector Retrieval Engine...")
        self._song_map: Dict[int, Song] = {}
        self._tfidf_vectors: List[Dict[str, float]] = []
        self._idf: Dict[str, float] = {}
        self._is_indexed = False

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def build_index(self, songs: List[Song]):
        """Builds the vocabulary, IDF weights, and normalized document vectors."""
        if not songs:
            return

        self._song_map = {idx: s for idx, s in enumerate(songs)}
        documents = [self._tokenize(f"{s.title} {s.artist.get_name()}") for s in songs]
        n_docs = len(documents)

        # 1. Compute Document Frequencies
        df: Dict[str, int] = Counter()
        for doc in documents:
            for term in set(doc):
                df[term] += 1

        # 2. Compute Smoothed IDF
        self._idf = {term: math.log((1 + n_docs) / (1 + freq)) + 1.0 for term, freq in df.items()}

        # 3. Compute Normalized TF-IDF Vector for each song
        self._tfidf_vectors = []
        for doc in documents:
            tf = Counter(doc)
            vec: Dict[str, float] = {}
            norm_sq = 0.0

            for term, count in tf.items():
                tfidf_val = count * self._idf[term]
                vec[term] = tfidf_val
                norm_sq += tfidf_val ** 2

            norm = math.sqrt(norm_sq) or 1.0
            # Unit normalization for fast dot-product cosine similarity
            normalized_vec = {term: val / norm for term, val in vec.items()}
            self._tfidf_vectors.append(normalized_vec)

        self._is_indexed = True
        print(f"[AI Engine] Indexed {len(self._song_map)} tracks into Vector Space.")

    def _cosine_similarity(self, vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        """Computes dot product between two unit-normalized sparse vectors."""
        if len(vec_a) > len(vec_b):
            vec_a, vec_b = vec_b, vec_a
        return sum(val * vec_b.get(term, 0.0) for term, val in vec_a.items())

    def _maximal_marginal_relevance(
        self,
        query_vec: Dict[str, float],
        candidate_indices: List[int],
        top_k: int = 5,
        lambda_param: float = 0.65
    ) -> List[int]:
        """
        MMR slate generation:
        MR = argmax [ λ * Sim(doc, query) - (1 - λ) * max(Sim(doc, selected)) ]
        """
        if not candidate_indices:
            return []

        selected: List[int] = []
        candidates = list(candidate_indices)

        for _ in range(min(top_k, len(candidates))):
            best_score = -float("inf")
            best_idx = None

            for cand in candidates:
                sim_to_query = self._cosine_similarity(query_vec, self._tfidf_vectors[cand])

                if not selected:
                    cross_sim = 0.0
                else:
                    cross_sim = max(
                        self._cosine_similarity(self._tfidf_vectors[cand], self._tfidf_vectors[sel])
                        for sel in selected
                    )

                mmr_score = lambda_param * sim_to_query - (1 - lambda_param) * cross_sim
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_idx = cand

            if best_idx is not None:
                selected.append(best_idx)
                candidates.remove(best_idx)

        return selected

    def recommend_similar(self, seed_song: Song, all_songs: List[Song], top_k: int = 5) -> List[Song]:
        if not self._is_indexed or len(all_songs) != len(self._song_map):
            self.build_index(all_songs)

        # 1. Vectorize seed song query
        query_tokens = self._tokenize(f"{seed_song.title} {seed_song.artist.get_name()}")
        tf = Counter(query_tokens)
        query_vec: Dict[str, float] = {}
        norm_sq = 0.0

        for term, count in tf.items():
            if term in self._idf:
                val = count * self._idf[term]
                query_vec[term] = val
                norm_sq += val ** 2

        norm = math.sqrt(norm_sq) or 1.0
        query_vec = {t: v / norm for t, v in query_vec.items()}

        # 2. Stage 1: Candidate Generation via Cosine Similarity
        scores = []
        for idx, vec in enumerate(self._tfidf_vectors):
            if self._song_map[idx].id != seed_song.id:
                sim = self._cosine_similarity(query_vec, vec)
                scores.append((idx, sim))

        scores.sort(key=lambda x: x[1], reverse=True)
        candidate_pool = [idx for idx, _ in scores[: top_k * 3]]

        # 3. Stage 2: MMR Diversity Re-Ranking
        ranked_indices = self._maximal_marginal_relevance(query_vec, candidate_pool, top_k=top_k)

        return [self._song_map[i] for i in ranked_indices]

    def recommend(self, all_songs: List[Song]) -> List[Song]:
        if not self._is_indexed:
            self.build_index(all_songs)
        return all_songs[:5]