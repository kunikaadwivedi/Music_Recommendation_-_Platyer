# test_spotify.py
from services.spotify_client import SpotifyClient

def main():
    print("Testing Spotify API authentication...")
    client = SpotifyClient()
    
    query = "genre:electronic year:2024"
    print(f"Fetching real tracks for query: '{query}'...")
    tracks = client.search_tracks(query=query, limit=5)
    
    print(f"\nSuccessfully fetched {len(tracks)} live tracks from Spotify:")
    for idx, t in enumerate(tracks, start=1):
        artist_name = t["artists"][0]["name"]
        popularity = t.get("popularity", "N/A")
        print(f"{idx}. {t['name']} by {artist_name} (Popularity: {popularity})")

if __name__ == "__main__":
    main()