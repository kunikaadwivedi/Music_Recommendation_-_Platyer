# services/spotify_client.py
from __future__ import annotations
from typing import List, Dict, Optional, TYPE_CHECKING
import requests
import base64
import time
from config import settings

if TYPE_CHECKING:
    from entities.song import Song
    from entities.artist import Artist
    from entities.album import Album


class SpotifyClient:
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    BASE_URL = "https://api.spotify.com/v1"

    def __init__(self):
        settings.validate()
        self._client_id = settings.SPOTIFY_CLIENT_ID
        self._client_secret = settings.SPOTIFY_CLIENT_SECRET
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0.0

    def _get_auth_header(self) -> Dict[str, str]:
        """Fetch or refresh bearer token using client credentials flow."""
        if time.time() >= self._token_expires_at:
            auth_str = f"{self._client_id}:{self._client_secret}"
            b64_auth = base64.b64encode(auth_str.encode()).decode()

            headers = {
                "Authorization": f"Basic {b64_auth}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {"grant_type": "client_credentials"}
            
            response = requests.post(self.TOKEN_URL, headers=headers, data=data)
            if response.status_code != 200:
                print(f"\n[Spotify Auth Error Details]: status={response.status_code}")
                print(f"Response body: {response.text}\n")
            
            response.raise_for_status()

            res_data = response.json()
            self._access_token = res_data["access_token"]
            self._token_expires_at = time.time() + res_data["expires_in"] - 60

        return {"Authorization": f"Bearer {self._access_token}"}

    def search_tracks(self, query: str = "rock 2024", limit: int = 10) -> List[Dict]:
        """Stream live tracks via Spotify Search API."""
        headers = self._get_auth_header()
        url = f"{self.BASE_URL}/search"
        
        # Ensure limit is strictly an int within [1, 50]
        safe_limit = max(1, min(int(limit), 50))
        
        params = {
            "q": str(query),
            "type": "track",
            "market": "US",
            "limit": safe_limit
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"[Spotify Search Warning] Status: {response.status_code}, Body: {response.text}")
        response.raise_for_status()
        
        items = response.json().get("tracks", {}).get("items", [])
        return items