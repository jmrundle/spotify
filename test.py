# Adds tracks to a playlist

import sys

import spotipy
import spotipy.util as util


if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()



scope = "playlist-modify-public user-top-read"
token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(auth=token)
tracks = sp.current_user_top_tracks(time_range="short_term", limit=50)["items"]
playlist_id = sp.user_playlist_create(username, "test")["id"]

uris = [track["uri"] for track in tracks]

sp.user_playlist_add_tracks(username, playlist_id, tracks)
