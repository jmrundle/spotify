"""
Creates a queue from the songs in a select playlist, with a preference towards songs recently added
"""

from wrapper import SpotifyWrapper
from util import random_weighted_select
from random import shuffle
import sys


PL_FILE = ".queue-playlist-id"


def get_playlist_id():
    """
    Load Spotify Playlist ID from a cache file
    """
    pl_id = None
    with open(PL_FILE, 'r') as pl_file:
        pl_id = pl_file.readline()
    return pl_id


def save_playlist_id(pl_id):
    """
    Save Spotify Playlist ID to a cache file
    """
    with open(PL_FILE, 'w+') as pl_file:
        pl_file.write(pl_id)


def create_playlist(sp, name):
    """
    Creates a playlist for a user, then returns that playlist ID
    """
    playlist = sp.create_playlist(name)
    return playlist["id"]


def print_playlists(playlists):
    """
    :param playlists: list of Spotify simplified playlist objects
    """
    for i, playlist in enumerate(playlists):
        print(i+1, playlist["name"], end=" ")

        if playlist["description"]:
            print("(" + playlist["description"] + ")", end="")

        print()


def select_tracks(playlist_tracks, limit):
    """
    :param tracks: list of customized JSON playlist track objects
    :param limit: number of tracks to select
    """
    # select with preference to newer tracks
    tracks = playlist_tracks[::-1]
    tracks = random_weighted_select(tracks, limit=limit)
    shuffle(tracks)
    return tracks


def get_all_tracks(sp):
    """
    Get all of the tracks in a playlist (bypassing spotify's hard limit of 100 tracks per request)
    """
    fields = "items(track(uri),added_at),total"

    resp = sp.get_tracks(playlist_id, fields=fields)
    tracks = resp["items"]
    num_tracks = len(tracks)
    total = resp["total"]

    while num_tracks < total:
        resp = sp.get_tracks(playlist_id, fields=fields, offset=num_tracks)
        tracks.extend(resp["items"])
        num_tracks += len(resp["items"])

    return tracks


if __name__ == "__main__":
    """
    First, get all of the playlists for a user
    
    Then, have user select from them as the 'source' of the queue
    
    The program will then randomly select 100 songs with a preference towards
    songs recently added, then shuffle those songs for good measure
    
    Finally, the 100 songs are used to replace the contents of chosen playlist
    
    NOTE: the chosen playlist can be modified each time program is executed,
    via a second command line arg which specifies the name of the new playlist
    """

    # authorize if necessary
    sp = SpotifyWrapper("playlist-read-private playlist-modify-public")

    # get playlist ID from cache file (returns None if cache unavailable)
    queue_pl_id = get_playlist_id()

    # create playlist if necessary
    if queue_pl_id is None or len(sys.argv) > 1:
        name = sys.argv[1] if len(sys.argv) > 1 else "Queue"
        queue_pl_id = create_playlist(sp, name)
        save_playlist_id(queue_pl_id)

    playlists = sp.get_playlists()["items"]

    print_playlists(playlists)
    i = int(input("Select Playlist: ")) - 1

    # get the tracks for the chosen playlist, then filter to keep just track URI's
    playlist = playlists[i]
    playlist_id = playlist["id"]
    tracks = get_all_tracks(sp)
    tracks = select_tracks(tracks, 100)
    track_uris = [track["track"]["uri"] for track in tracks]

    # update playlist
    resp = sp.update_playlist(queue_pl_id, track_uris)

    if 200 <= resp.status_code < 400:
        print("Successfully created playlist")
    else:
        print("Response raised " + resp.status_code + " error code.")
