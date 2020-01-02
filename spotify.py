"""
Goal:
    - make program that tracks your music listening habits
    - user is encouraged to skip songs they aren't interested in

cron job to run every 2 seconds or so (the "sampling rate" is adjustable)


import spotipy


first time:
    - authorize user on a localhost connection
    - generate a token
next times:
    - get tokens from file
    - refresh tokens if necessary
    

every time:
    - get current track information (track name, genre, timestamp)
    - update statistics
        - make a database entry timestamp for that user, song, and time
    - update token file



separate program:
    - authorize
    - calculate metric which accounts for how often a person listens to certain songs
    - songs listened to infrequently are pooled into a group of songs that the program suggests the user remove from playlist
    - a report is generated upon request that details most popular songs by seconds listened to, etc.
"""




import requests
import json
from os import path


BASE = "https://api.spotify.com"
CLIENT_ID = "3ef02e948f334570b661cbfe781b941a"
CLIENT_SECRET = "bca8bff649c84dcb8c3dfde7ec0efc4c"


class Authentication:
    cache_file = ".spotify-token"

    def __init__(self, client_id, client_secret, redirect_uri, trace=False):
        self.client_id      = client_id
        self.client_secret  = client_secret
        self.redirect_uri   = redirect_uri

        self.access_token  = None
        self.refresh_token = None
        self.token_expired = True

        self.trace = False

    def _get(self, endpoint, params=None):
        headers = { 'Content-Type': 'application/json' }

        resp = requests.get(BASE + endpoint, headers=headers, params=params)
        
        if self.trace:
            print("GET", BASE + endpoint)
            print("Headers:", headers)
            print("Params:", json.dumps(params, 4))
            print("Response:", resp.json())

        return resp
    
    def authorize():
        """
        - Use Authorization Code flow to generate an access token and refresh token
        - Once access token expires, use refresh token to generate a new token
        """
        params = {
            'response_type':    "code",
            'client_id':        self.client_id,
            'redirect_uri':     self.redirect_uri
        }
        
        res = self._get("/authorize", params=params)
    
    def get_token():
        endpoint = "/api/token"
        
        if path.exists(self.cache_file):
            with open(CACHE_FILE, 'r') as json_file:
                data = json.load(json_file)
                access_token = data['access_token']
                refresh_token = data['refresh_token']
                expiration_time = data['expiration_time']

    def load_from_cache():
        data = {}
        with open(self.cache_file, 'r') as json_file:
            data = json.load(json_file)
        return data
    
    @staticmethod
    def save_to_cache(data):
        with open(CACHE_FILE, 'w') as json_file:
            json.dumps(data, json_file)
            
        
    def refresh_token():
        pass


class App:

    def __init__(self):
        self.authentication = Authentication(CLIENT_ID, CLIENT_SECRET)
        self.authentication.authorize()
        
