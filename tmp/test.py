# shows audio analysis for the given track

from __future__ import print_function
import spotipy
import spotipy.util as util

# ====== connect to API ======
username = "jackrundle530"
scope = "user-read-currently-playing"
redirect_uri = "http://localhost:8888/callback/"
client_id = '3ef02e948f334570b661cbfe781b941a'
client_secret = 'bca8bff649c84dcb8c3dfde7ec0efc4c'
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
sp = spotipy.Spotify(auth=token)

# ===== get relevant data from spotify JSON object ======
# info about current song
currentsong = sp.currently_playing()
song_name = currentsong['item']['name']
song_artists = currentsong['item']['artists']
track_id = "spotify:track:" + currentsong['item']['id']
progress = currentsong['progress_ms'] // 1000
duration = currentsong['item']['duration_ms'] // 1000
# audio analysis about current playing song
analysis = sp.audio_analysis(track_id)
sections = analysis['sections']


def format_time(seconds):
	left_seconds = seconds % 60
	minutes = seconds // 60
	
	two = lambda num: str(num) if num >= 10 else "0" + str(num)
	
	if minutes < 60:
		return str(minutes) + ":" + two(left_seconds)
	else:
		left_minutes = minutes % 60
		hours = minutes // 60
		return str(hours) + ":" + two(left_minutes) + ":" + two(left_seconds)


print("Now playing: ", song_name)
print("Artists: ", ", ".join(map(lambda a: a['name'], song_artists)))
print("Progress: ", format_time(progress), " / ", format_time(duration))

for section in sections:
	if progress <= section['start'] + section['duration']:
		print("Loudness: ", section['loudness'])
		print("Key: ", section['key'])
		break
