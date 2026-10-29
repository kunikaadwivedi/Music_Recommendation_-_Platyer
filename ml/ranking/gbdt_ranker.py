# ml/ranking/gbdt_ranker.py
from typing import List, Dict, Any
import numpy as np
import lightgbm as lgb
from entities.song import Song
from entities.user import User


class GBDTRanker:
    """
    Second-Stage Personalization Ranker using LightGBM.
    Scores candidates based on user affinity, track metadata, and real-time interaction features.
    """
    FEATURE_NAMES = [
        "retrieval_similarity",
        "popularity",
        "user_skip_rate",
        "duration_seconds",
        "artist_familiarity"
    ]

    def __init__(self):
        self.model: lgb.LGBMRegressor = lgb.LGBMRegressor(
            n_estimators=50,
            learning_rate=0.05,
            max_depth=4,
            random_state=42
        )
        self._is_trained = False
        self._bootstrap_synthetic_model()

    def _extract_features(
        self,
        user: User,
        candidates: List[Song],
        similarities: List[float]
    ) -> np.ndarray:
        """Constructs the real-time feature matrix for candidate scoring."""
        feature_rows = []
        user_skip_rate = getattr(user, "skip_rate", 0.15)
        played_artists = getattr(user, "preferred_artists", set())

        for song, sim in zip(candidates, similarities):
            artist_familiarity = 1.0 if song.artist.get_name() in played_artists else 0.0
            popularity = getattr(song, "popularity", 50.0) / 100.0
            duration = float(song.duration_in_seconds)

            feature_rows.append([
                float(sim),
                float(popularity),
                float(user_skip_rate),
                float(duration),
                float(artist_familiarity)
            ])

        return np.array(feature_rows, dtype=np.float32)

    def _bootstrap_synthetic_model(self):
        """Pre-trains model on initial behavioral priors so cold-start inference works immediately."""
        np.random.seed(42)
        n_samples = 2000
        # Synthetic interactions: similarity (0-1), popularity (0-1), skip_rate (0-1), duration (s), familiarity (0-1)
        sim = np.random.uniform(0.1, 1.0, n_samples)
        pop = np.random.uniform(0.1, 1.0, n_samples)
        skip = np.random.uniform(0.0, 0.5, n_samples)
        dur = np.random.uniform(120, 360, n_samples)
        fam = np.random.choice([0.0, 1.0], size=n_samples, p=[0.7, 0.3])

        X = np.column_stack([sim, pop, skip, dur, fam])
        # Engagement ground truth: reward high similarity, familiarity, and popularity; penalize high user skip rate
        y = (0.5 * sim) + (0.3 * pop) + (0.2 * fam) - (0.4 * skip) + np.random.normal(0, 0.05, n_samples)

        self.model.fit(X, y)
        self._is_trained = True

    def rank(
        self,
        user: User,
        candidates: List[Song],
        similarities: List[float],
        top_k: int = 5
    ) -> List[Song]:
        """Scores candidate pool using GBDT and returns ranked top_k list."""
        if not candidates:
            return []

        X = self._extract_features(user, candidates, similarities)
        predicted_scores = self.model.predict(X)

        # Sort candidate indices by predicted engagement score descending
        ranked_indices = np.argsort(-predicted_scores)[:top_k]
        return [candidates[i] for i in ranked_indices]