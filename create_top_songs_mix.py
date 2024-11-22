import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Fetch Spotify credentials from environment variables
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:8888/callback")  # Default if not set

# Ensure environment variables are set
if not CLIENT_ID or not CLIENT_SECRET:
    raise EnvironmentError("Please set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables.")

# Initialize Spotify client with user authentication
scope = "playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))

# Artists to include in the playlist
artists = ["Yago Oproprio", "Criolo", "Black Alien"]

# Playlist name
playlist_name = "Top Tracks Mix: Yago Oproprio, Criolo, Black Alien"

# Fetch top tracks for each artist
playlist_tracks = []
for artist in artists:
    results = sp.search(q=f"artist:{artist}", type="artist", limit=1)
    if results['artists']['items']:
        artist_id = results['artists']['items'][0]['id']
        top_tracks = sp.artist_top_tracks(artist_id, country='US')
        for track in top_tracks['tracks'][:10]:  # Adjust for more tracks
            playlist_tracks.append(track['uri'])  # Spotify URI for the track

# Create a new playlist
user_id = sp.current_user()["id"]  # Get the current user's Spotify ID
new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)

# Add tracks to the playlist
if playlist_tracks:
    sp.playlist_add_items(playlist_id=new_playlist["id"], items=playlist_tracks)
    print(f"Playlist '{playlist_name}' created successfully!")
else:
    print("No tracks found to add to the playlist.")

