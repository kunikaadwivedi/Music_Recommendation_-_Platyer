# api/main.py
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from music_streaming_system import MusicStreamingSystem
from strategy.recommendation.two_stage_ranker_strategy import TwoStageRankerStrategy
from entities.user import User
from enums.subscription_tier import SubscriptionTier

app = FastAPI(
    title="High-Performance Music Recommendation Microservice",
    version="1.0.0",
    description="Two-Stage (Vector Retrieval + GBDT Re-Ranking) recommendation engine."
)

system = MusicStreamingSystem.get_instance()
two_stage_strategy = TwoStageRankerStrategy()

# Pydantic Schemas
class SongResponse(BaseModel):
    id: str
    title: str
    artist: str
    duration_seconds: int
    spotify_url: Optional[str] = None
    preview_url: Optional[str] = None

class RecommendationRequest(BaseModel):
    user_id: str
    seed_song_id: str
    subscription_tier: str = "PREMIUM"
    top_k: int = 5

class IngestRequest(BaseModel):
    query: str = "electronic 2024"
    limit: int = 10

# Startup Event: Ingest and index initial data
@app.on_event("startup")
def startup_event():
    print("[API] Initializing catalog and ML models...")
    try:
        system.ingest_from_spotify(query="top hits", limit=10)
    except Exception as e:
        print(f"[API Warning] Ingestion fallback active: {e}")
    catalog = list(system._songs.values())
    if catalog:
        two_stage_strategy.build_index(catalog)
        system._recommendation_service.set_strategy(two_stage_strategy)

# Middleware for latency tracking
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time_ms = (time.perf_counter() - start_time) * 1000
    response.headers["X-Inference-Time-MS"] = f"{process_time_ms:.2f}"
    return response

@app.post("/v1/ingest", tags=["Data Pipeline"])
def ingest_live_tracks(req: IngestRequest):
    count = system.ingest_from_spotify(query=req.query, limit=req.limit)
    catalog = list(system._songs.values())
    two_stage_strategy.build_index(catalog)
    return {"status": "success", "tracks_ingested": count, "total_catalog": len(catalog)}

@app.get("/v1/catalog", response_model=List[SongResponse], tags=["Catalog"])
def get_catalog():
    return [
        SongResponse(
            id=s.id,
            title=s.title,
            artist=s.artist.get_name(),
            duration_seconds=s.duration_in_seconds,
            spotify_url=s.spotify_url,
            preview_url=s.preview_url
        )
        for s in system._songs.values()
    ]

@app.post("/v1/recommend", response_model=List[SongResponse], tags=["Inference"])
def recommend_tracks(req: RecommendationRequest):
    if req.seed_song_id not in system._songs:
        raise HTTPException(status_code=404, detail="Seed song ID not found in catalog.")

    seed_song = system._songs[req.seed_song_id]
    tier = SubscriptionTier.PREMIUM if req.subscription_tier.upper() == "PREMIUM" else SubscriptionTier.FREE
    user = User(req.user_id, tier, 0)

    catalog = list(system._songs.values())
    ranked_songs = two_stage_strategy.recommend_for_user(user, seed_song, catalog, top_k=req.top_k)

    return [
        SongResponse(
            id=s.id,
            title=s.title,
            artist=s.artist.get_name(),
            duration_seconds=s.duration_in_seconds,
            spotify_url=s.spotify_url,
            preview_url=s.preview_url
        )
        for s in ranked_songs
    ]