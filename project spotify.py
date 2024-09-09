import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Get Spotify API credentials from environment variables
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'playlist-modify-public playlist-modify-private'

# Authenticate and create a Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

def create_playlist(user_id, playlist_name):
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    return playlist['id']

def search_track(track_name):
    result = sp.search(q=track_name, type='track', limit=1)
    tracks = result['tracks']['items']
    if tracks:
        return tracks[0]['id']
    else:
        return None

def add_tracks_to_playlist(playlist_id, track_ids):
    sp.playlist_add_items(playlist_id, track_ids)

def main():
    # Input list of songs
    song_list = [
        "kal ho na ho", "chak de india"
    ]

    # Get current user ID
    user_id = sp.current_user()['id']
    
    # Playlist name
    playlist_name = 'My Custom Playlist2'

    # Create playlist
    playlist_id = create_playlist(user_id, playlist_name)
    print(f'Playlist "{playlist_name}" created with ID: {playlist_id}')

    # Search for tracks and add them to the playlist
    track_ids = []
    for song in song_list:
        track_id = search_track(song)
        if track_id:
            track_ids.append(track_id)
        else:
            print(f'Track not found: {song}')

    if track_ids:
        add_tracks_to_playlist(playlist_id, track_ids)
        print(f'Tracks added to playlist: {playlist_id}')
    else:
        print('No tracks found to add to the playlist.')

if __name__ == "__main__":
    main()
