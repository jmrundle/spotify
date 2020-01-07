"""
Custom Daily-Mix implementation
"""
from wrapper import SpotifyWrapper
from util import random_weighted_select, random_select
from os import environ
import json


PLAYLIST_NAME = "Custom Daily Mix"
PLAYLIST_DESCRIPTION = "Programmatically generated daily mix"


def aggregate_top_genres(artists, limit=3):
    """Aggregate a list of the top genres based on artist preferences"""
    genre_map = dict()

    # get count of each genre
    for artist in artists:
        for genre in artist["genres"]:
            genre_map[genre] = genre_map.get(genre, 0) + 1

    # sort genres by frequency
    genres = sorted(genre_map.keys(), key=lambda key: genre_map[key], reverse=True)

    # take top 3
    return genres[:limit]


def median_popularity(artists):
    """
    Calculates the median popularity of each artist

    Could be O(n), but O(n*logn) keeps things simple and works fine
    """
    popularity = [artist["popularity"] for artist in artists]
    popularity = sorted(popularity)
    return popularity[len(popularity) // 2]


def get_recommendations(sp, top_tracks, top_artists, limit=15):
    top_track_ids = [track["id"] for track in top_tracks]

    # seed recommendations
    seed_tracks = random_weighted_select(top_track_ids, 2)
    seed_genres = aggregate_top_genres(top_artists, 3)
    target_popularity = median_popularity(top_artists)

    # songs to add to playlist
    recommendations = sp.get_recommendations(market="US",
                                             seed_tracks=seed_tracks,
                                             seed_genres=seed_genres,
                                             target_popularity=target_popularity,
                                             limit=50)["tracks"]

    rec_ids = [rec["uri"] for rec in recommendations]
    return random_weighted_select(rec_ids, limit=limit)


def get_new_tracks(sp, new_albums, top_artists, limit=10):
    """Gets a list of new tracks somewhat tailored to the user"""
    top_genres = aggregate_top_genres(top_artists, 10)
    album_ids  = [album["id"] for album in new_albums]

    albums = sp.get_albums(album_ids)["albums"]

    artist_tracks = dict()
    for album in albums:
        for track in album["tracks"]["items"]:
            for artist in track["artists"]:
                if artist["id"] in artist_tracks:
                    artist_tracks[artist["id"]].append(track["uri"])
                else:
                    artist_tracks[artist["id"]] = [track["uri"]]

    artists = sp.get_artists(list(artist_tracks.keys()))
    popularity = dict()
    artist_matches = list()
    for artist in artists["artists"]:
        popularity[artist["id"]] = artist["popularity"]

        if any(genre in top_genres for genre in artist["genres"]):
            artist_matches.append(artist["id"])

    artist_matches = sorted(artist_matches, reverse=True, key=lambda a: popularity[a])

    tracks = list()
    for artist_id in artist_matches:
        tracks += artist_tracks[artist_id]

    return random_select(tracks, limit=10)


def update_playlist(sp, uris):
    if not environ.get("PLAYLIST_ID"):
        playlist_id = sp.create_playlist(PLAYLIST_NAME, description=PLAYLIST_DESCRIPTION)["id"]
        environ["PLAYLIST_ID"] = playlist_id
        print(f"Created playlist {playlist_id}")

        sp.add_tracks(playlist_id, uris)

    else:
        playlist_id = environ["PLAYLIST_ID"]
        sp.update_playlist(playlist_id, uris)

    print("Loaded playlist with the following tracks:")
    print("\n".join(f"{i}: {turi}" for i, turi in enumerate(uris)))

if __name__ == '__main__':
    # Composition of Playlist
    #   20 random songs from short-term favorites
    #   15 song recommendations
    #   10 songs from recently released
    #   1  song from 5 short-term favorite artists

    # Recommendation seed info
    #
    #   Seed Tracks: top 2 tracks
    #   Seed Genre: top 3 genres
    #   Target Popularity:  avg popularity of artists
    #
    #   Use this to generate 50 songs

    sp = SpotifyWrapper("user-top-read playlist-modify-public")

    # get top tracks and artists
    top_tracks = sp.get_top_tracks(time_range="short_term", limit=50)["items"]
    top_artists = sp.get_top_artists(time_range="short_term", limit=50)["items"]
    new_albums = sp.get_new_albums(limit=50)["albums"]["items"]

    top_track_uris = [track["uri"] for track in top_tracks]

    # songs to add to playlist
    favorite_tracks = random_weighted_select(top_track_uris, 20)
    recommendations = get_recommendations(sp, top_tracks, top_artists, 15)
    new_tracks = get_new_tracks(sp, new_albums, top_artists, 10)

    songs = favorite_tracks + recommendations + new_tracks

    update_playlist(sp, songs)







