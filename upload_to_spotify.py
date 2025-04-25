import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_spotify_client():
    """Set up and return a Spotify client with proper authorization."""
    # You'll need to register your app on Spotify Developer Dashboard to get these
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")

    # Set up authentication with necessary scopes
    scope = "playlist-modify-public playlist-modify-private"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    ))

    return sp

def create_playlist(sp, name, description=""):
    """Create a new playlist and return its ID."""
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(
        user=user_id,
        name=name,
        public=False,
        description=description
    )
    print(f"Created playlist: {name} (ID: {playlist['id']})")
    return playlist['id']

def add_track_to_playlist(sp, playlist_id, track_uri):
    """Add a track to the specified playlist."""
    sp.playlist_add_items(playlist_id, [track_uri])
    print(f"Added track {track_uri} to playlist {playlist_id}")

def search_track(sp, track_name, artist=None):
    """Search for a track on Spotify and return its URI."""
    query = track_name
    if artist:
        query += f" artist:{artist}"

    results = sp.search(q=query, type="track", limit=1)

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        print(f"Found track: {track['name']} by {track['artists'][0]['name']}")
        return track['uri']
    else:
        print(f"No track found for query: {query}")
        return None

def main():
    # Set up the Spotify client
    sp = setup_spotify_client()

    # Create a new playlist or use an existing one
    create_new = input("Create a new playlist? (y/n): ").lower() == 'y'

    if create_new:
        playlist_name = input("Enter playlist name: ")
        playlist_description = input("Enter playlist description (optional): ")
        playlist_id = create_playlist(sp, playlist_name, playlist_description)
    else:
        # Show list of user's playlists to choose from
        playlists = sp.current_user_playlists()
        print("Your playlists:")
        for i, playlist in enumerate(playlists['items']):
            print(f"{i+1}. {playlist['name']} (ID: {playlist['id']})")

        playlist_index = int(input("Enter the number of the playlist to use: ")) - 1
        playlist_id = playlists['items'][playlist_index]['id']

    # Note: Since we can't upload directly to Spotify, we'd need to search for the track
    print("\nNOTE: Spotify doesn't allow direct uploads of local MP3 files.")
    print("To add your track to Spotify, you need to distribute it through a service like DistroKid or TuneCore first.")
    print("Once your track is on Spotify, you can search for it and add it to your playlist.")

    # For demonstration, let's search for a track
    search = input("Would you like to search for a track to add to your playlist? (y/n): ").lower() == 'y'
    if search:
        track_name = input("Enter track name: ")
        artist_name = input("Enter artist name (optional): ")
        track_uri = search_track(sp, track_name, artist_name)

        if track_uri:
            add_track_to_playlist(sp, playlist_id, track_uri)
            print("Track added successfully!")
        else:
            print("Could not find the track on Spotify.")

if __name__ == "__main__":
    main()
