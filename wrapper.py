"""
Wrapper for a few useful methods from the Spotify API
"""

from oauth2 import SpotifyOAuth
import webbrowser
from os import environ
import json
import requests
import time


BASE = "https://api.spotify.com"


class SpotifyWrapper:

    def __init__(self, scope, client_id=None, client_secret=None, redirect_uri=None):       
        if client_id is None:
            client_id = environ.get("SPOTIFY_CLIENT_ID", "3ef02e948f334570b661cbfe781b941a")
        if client_secret is None:
            client_secret = environ.get("SPOTIFY_CLIENT_SECRET", "bca8bff649c84dcb8c3dfde7ec0efc4c")
        if redirect_uri is None:
            redirect_uri = environ.get("SPOTIFY_REDIRECT_URI", "http://localhost:8000/callback")

        cache_path = "spotify-token.json"
        
        self.auth = SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope, cache_path=cache_path)

        self.trace = False
        
    def get_access_token(self):
        token = self.auth.get_cached_token()

        if token is None:
            url = self.auth.get_authorize_url()
            webbrowser.open(url)
            print("After you authenticate and give permission for this app to access various scopes,")
            print("  you will be redirected to a URL.")
            url = input("Enter that URL here: ")

            code = self.auth.parse_response_code(url)
            token = self.auth.get_access_token(code)

        return token["access_token"]

    def get_headers(self):
        token = self.get_access_token()

        return {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
            }
        
    def _get(self, endpoint, **params):
        headers = self.get_headers()

        if self.trace:
            print("GET ", BASE + endpoint)
            print("Headers: ", json.dumps(headers, indent=4))
            print("Params: ", json.dumps(params, indent=4))
        
        resp = requests.get(BASE + endpoint, headers=headers, params=params)
        return resp.json()
    
    def _post(self, endpoint, **payload):
        headers = self.get_headers()
        resp = requests.post(BASE + endpoint, headers=headers, payload=payload)
        return resp.json()

    def _put(self, endpoint, payload, **params):
        headers = self.get_headers()
        resp = requests.put(BASE + endpoint, headers=headers, payload=payload, params=params)
        return resp.json()
    
    def get_user_id(self):
        return self._get("/v1/me")["id"]

    def get_top_artists(self, time_range='short_term', limit=50):
        #user-top-read
        return self._get("/v1/me/top/artists", time_range=time_range, limit=limit)

    def get_top_tracks(self, time_range='short_term', limit=50):
        #user-top-read
        return self._get("/v1/me/top/tracks", time_range=time_range, limit=limit)

    def make_playlist(self, name):
        #playlist-modify-public
        user_id = self.get_user_id()
        return self._post(f"/v1/user/{user_id}/playlists/", name=name)

    def update_playlist(self, playlist_id, track_uris):
        #playlist-modify-public
        tracks = ",".join(track_uris)
        return self._put(f"/v1/playlists/{playlist_id}/tracks/", uris=tracks)

    def get_new_releases(self, limit=10, country='US'):
        return self._get("/v1/browse/new-releases", country=country, limit=limit)
        
    def get_recommendations(self, seed, **kwargs):
        artists = ",".join(seed.get('artists', []))
        genres = ",".join(seed.get('genres', []))
        tracks = ",".join(seed.get('tracks', []))

        return self_get("/v1/recommendations", seed_artists=artists, seed_genres=genres, seed_tracks=tracks, **kwargs)
    
        
        



