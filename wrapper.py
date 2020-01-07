"""
Wrapper for a few useful methods from the Spotify API
"""

from oauth2 import SpotifyOAuth
import webbrowser
from os import environ
import json
import requests


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
        resp = requests.get(BASE + endpoint, headers=headers, params=params)

        if self.trace:
            print("GET ", BASE + endpoint)
            print("Headers: ", json.dumps(headers, indent=4))
            print("Params: ", json.dumps(params, indent=4))
            print("Response: ", json.dumps(resp.json(), indent=4))

        return resp.json()
    
    def _post(self, endpoint, data=None):
        headers = self.get_headers()
        resp = requests.post(BASE + endpoint, headers=headers, data=data)

        if self.trace:
            print("POST ", BASE + endpoint)
            print("Headers: ", json.dumps(headers, indent=4))
            print("Data: ", json.dumps(data, indent=4))
            print("Response: ", json.dumps(resp.json(), indent=4))

        return resp.json()

    def _put(self, endpoint, data=None, **params):
        headers = self.get_headers()
        resp = requests.put(BASE + endpoint, headers=headers, data=data, params=params)

        if self.trace:
            print("PUT ", BASE + endpoint)
            print("Headers: ", json.dumps(headers, indent=4))
            print("Params: ", json.dumps(params, indent=4))
            print("Payload: ", json.dumps(data, indent=4))
            print("Response: ", json.dumps(resp.json(), indent=4))

        return resp.json()
    
    def get_user_id(self):
        return self._get("/v1/me")["id"]

    def get_top_artists(self, time_range='short_term', limit=50):
        # user-top-read
        return self._get("/v1/me/top/artists", time_range=time_range, limit=limit)

    def get_top_tracks(self, time_range='short_term', limit=50):
        # user-top-read
        return self._get("/v1/me/top/tracks", time_range=time_range, limit=limit)

    def get_new_releases(self, limit=10, country='US'):
        return self._get("/v1/browse/new-releases", country=country, limit=limit)
        
    def get_recommendations(self, seed_artists=None, seed_genres=None, seed_tracks=None, **kwargs):
        seed_artists = ",".join(seed_artists) if seed_artists else ""
        seed_genres = ",".join(seed_genres) if seed_genres else ""
        seed_tracks = ",".join(seed_tracks) if seed_tracks else ""
        return self._get("/v1/recommendations", seed_artists=seed_artists, seed_genres=seed_genres, seed_tracks=seed_tracks, **kwargs)

    def get_new_albums(self, country="US", limit=50):
        return self._get("/v1/browse/new-releases", country=country, limit=limit)

    def get_albums(self, ids, market="US"):
        ids = ",".join(ids[:20])
        return self._get("/v1/albums", ids=ids, market=market)

    def get_artists(self, ids):
        ids = ",".join(ids[:50])
        return self._get("/v1/artists", ids=ids)

    def create_playlist(self, name, public=True, description=""):
        user_id = self.get_user_id()
        data = {
            "name": name,
            "public": 'true' if public else 'false',
            "description": description
        }
        return self._post(f"/v1/users/{user_id}/playlists", data=json.dumps(data))

    def add_tracks(self, playlist_id, track_uris):
        uris = ",".join(track_uris)
        data = {"uris": uris}
        return self._post(f"/v1/playlists/{playlist_id}/tracks/", data=json.dumps(data))

    def update_playlist(self, playlist_id, track_uris):
        # playlist-modify-public
        uris = ",".join(track_uris)
        return self._put(f"/v1/playlists/{playlist_id}/tracks/", uris=uris)




