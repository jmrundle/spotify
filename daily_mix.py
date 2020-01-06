"""
Custom Daily-Mix implementation
"""
import SpotifyWrapper


sp = SpotifyWrapper("user-top-read")

top_tracks = sp.get_top_tracks(time_range="short_term", limit=50)
top_artists = sp.get_top_artists()


weighted_tracks = list()
tot = 0
for i, track in enumerate(top_tracks['items']):
    tot += (50 - i)
    info = [track['uri'], tot]
    weighted_tracks.append(info)



# Recommendation seed info
#
#   Seed Tracks: top 2 tracks
#   Seed Genre: top 3 genres
#   Target Popularity:  avg popularity of artists
#
#   Use this to generate 50 songs


for track in sp.get_top_tracks()["items"]:
    name = track["name"]
    artists = [artist["name"] for artist in track["artists"]]

    print(name, "(" + ", ".join(artists) + ")")
