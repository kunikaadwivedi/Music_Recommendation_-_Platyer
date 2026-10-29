# music_streaming_demo.py
from music_streaming_system import MusicStreamingSystem
from strategy.recommendation.vector_recommendation_strategy import VectorRecommendationStrategy
from entities.user import User
from enums.subscription_tier import SubscriptionTier

def main():
    system = MusicStreamingSystem.get_instance()

    print("==================================================")
    print(" 1. Ingesting Live Data Streams from Spotify ")
    print("==================================================")
    system.ingest_from_spotify(query="rock 2024", limit=15)
    system.ingest_from_spotify(query="electronic hits", limit=15)
    system.ingest_from_spotify(query="top pop", limit=15)
    
    catalog = list(system._songs.values())
    print(f"\nTotal catalog loaded: {len(catalog)} live songs across {len(system._artists)} artists.\n")

    print("==================================================")
    print(" 2. Initializing AI Vector Recommendation Engine ")
    print("==================================================")
    vector_strategy = VectorRecommendationStrategy()
    system._recommendation_service.set_strategy(vector_strategy)
    vector_strategy.build_index(catalog)

    # Pick a seed song from the catalog
    seed = catalog[0]
    print(f"\n>>> Seed Track: {seed} <<<\n")

    print("==================================================")
    print(" 3. Two-Stage Retrieval (ANN + MMR Re-Ranking) ")
    print("==================================================")
    recommendations = system.get_vector_recommendations(seed, top_k=5)

    for rank, track in enumerate(recommendations, start=1):
        print(f"Rank {rank}: {track.title} — {track.artist.get_name()}")

    print("\n==================================================")
    print(" 4. Playback System with Strategy & State Patterns ")
    print("==================================================")
    user = User("Alice", SubscriptionTier.PREMIUM, 0)
    player = system.get_player()
    
    # Load recommended tracks into player queue
    from entities.playlist import Playlist
    ai_playlist = Playlist("AI Recommendations")
    for track in recommendations:
        ai_playlist.add_track(track)

    player.load(ai_playlist, user)
    player.click_play()
    player.click_next()

if __name__ == "__main__":
    main()