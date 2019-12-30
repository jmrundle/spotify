import requests

BASE = "https://api.spotify.com"
CLIENT_ID = "3ef02e948f334570b661cbfe781b941a"
CLIENT_SECRET = "bca8bff649c84dcb8c3dfde7ec0efc4c"


class Authentication:

    def __init__(self, client_id, redirect_uri):
        self.client_id      = client_id
        self.redirect_uri   = redirect_uri

        self.access_token  = None
        self.refresh_token = None

    def authorize():
        """
        - Use Authorization Code flow to generate access token and refresh token
        - Once access token expires, use refresh token to generate a new token
        """
        endpoint= "/authorize"

        payload = {
            'response_type':    "code",
            'client_id':        self.client_id,
            'redirect_uri':     self.redirect_uri
        }
        
        res = requests.get(BASE + ENDPOINT, params=payload)

    def get_token():
        endpoint = "/api/token"
        
    def refresh_token():
        pass


class App:

    def __init__(self):
        self.authentication = Authentication(CLIENT_ID, CLIENT_SECRET)
        self.authentication.authorize()
        
