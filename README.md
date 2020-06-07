# Spotify API

### Utilities:
1. Custom Daily Mix
    - creates a playlist with a combination of new, favorite, and recommended songs
2. Weighted Queue generator
    - creates a queue of songs from a select playlist, with a preference towards songs recently added
### Notes:
- oauth.py is a slightly modified version of the [spotipy oauth2 file](https://github.com/plamere/spotipy/blob/master/spotipy/oauth2.py)

### TODO:
- setup cronjob to run daily_mix.py daily
- prompt for spotify username
