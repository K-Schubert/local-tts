import os
import webbrowser
import shutil
import json
from pathlib import Path
import subprocess

class AudioStreamingOptions:
    def __init__(self):
        self.mp3_path = os.path.join("output_audio", "combined_output.mp3")

    def validate_file(self):
        """Check if the MP3 file exists."""
        if not os.path.exists(self.mp3_path):
            print(f"Error: File not found at {self.mp3_path}")
            return False
        return True

    def show_options(self):
        """Display streaming options for MP3 files."""
        if not self.validate_file():
            return

        print("\n==== MP3 Streaming Options ====")
        print("Here are some ways to stream your MP3 file with screen-lock support:\n")

        options = [
            ("1", "Upload to SoundCloud", "Upload your MP3 to SoundCloud for streaming with screen locked"),
            ("2", "Upload to Google Drive and use an audio player app", "Store in Drive, play with VLC or other players"),
            ("3", "Upload to Dropbox and use Dropbox audio player", "Dropbox has built-in audio playback with screen lock support"),
            ("4", "Create a simple personal web server", "Host your files locally for streaming"),
            ("5", "Use a podcast hosting service", "Upload as a private podcast episode")
        ]

        for number, name, description in options:
            print(f"{number}. {name}\n   {description}\n")

        choice = input("Enter option number for more details (or 'q' to quit): ")
        self.handle_choice(choice)

    def handle_choice(self, choice):
        """Handle user selection."""
        if choice == 'q':
            return

        if choice == '1':
            self.soundcloud_option()
        elif choice == '2':
            self.google_drive_option()
        elif choice == '3':
            self.dropbox_option()
        elif choice == '4':
            self.local_server_option()
        elif choice == '5':
            self.podcast_option()
        else:
            print("Invalid option selected.")
            self.show_options()

    def soundcloud_option(self):
        """Provide details for SoundCloud uploading."""
        print("\n=== SoundCloud Upload ===")
        print("SoundCloud allows free uploads with background playback:")
        print("1. Create a SoundCloud account if you don't have one")
        print("2. You can set tracks as private if you don't want them public")
        print("3. The SoundCloud app supports background playback")

        open_site = input("Open SoundCloud upload page? (y/n): ")
        if open_site.lower() == 'y':
            webbrowser.open("https://soundcloud.com/upload")

    def google_drive_option(self):
        """Provide details for Google Drive with audio players."""
        print("\n=== Google Drive + Audio Player ===")
        print("Upload to Google Drive, then use an audio player app that can access Drive:")
        print("1. Upload your MP3 to Google Drive")
        print("2. Use VLC, BlackPlayer, Poweramp, or similar apps that can access cloud storage")
        print("3. These apps support background playback")

        open_site = input("Open Google Drive? (y/n): ")
        if open_site.lower() == 'y':
            webbrowser.open("https://drive.google.com")

    def dropbox_option(self):
        """Provide details for Dropbox audio playback."""
        print("\n=== Dropbox Audio Playback ===")
        print("Dropbox has built-in audio streaming with background playback:")
        print("1. Upload your audio to Dropbox")
        print("2. Use the Dropbox mobile app to play audio")
        print("3. Audio continues to play when your screen is locked")

        open_site = input("Open Dropbox? (y/n): ")
        if open_site.lower() == 'y':
            webbrowser.open("https://www.dropbox.com/home")

    def local_server_option(self):
        """Provide details for creating a local streaming server."""
        print("\n=== Personal Streaming Server ===")
        print("You can create a simple HTTP server to stream your audio:")
        print("1. Host your MP3s on a computer on your network")
        print("2. Access via a browser or audio streaming app on your phone")
        print("3. Most audio streaming apps support background playback")

        server_choice = input("Would you like to start a simple Python HTTP server for testing? (y/n): ")
        if server_choice.lower() == 'y':
            self.start_local_server()

    def podcast_option(self):
        """Provide details for using podcast hosting services."""
        print("\n=== Private Podcast ===")
        print("Upload your audio as a private podcast episode:")
        print("1. Use services like Anchor, PodBean, or Buzzsprout")
        print("2. Create a private feed only you can access")
        print("3. Listen using any podcast app with background playback")

        open_site = input("Open Anchor podcast creation page? (y/n): ")
        if open_site.lower() == 'y':
            webbrowser.open("https://anchor.fm/dashboard/episode/new")

    def start_local_server(self):
        """Start a simple HTTP server to stream audio files."""
        # Create a directory for serving files
        server_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_server")
        os.makedirs(server_dir, exist_ok=True)

        # Copy the MP3 file to the server directory
        if os.path.exists(self.mp3_path):
            shutil.copy2(self.mp3_path, os.path.join(server_dir, "audio.mp3"))

            # Create a simple HTML player
            html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Audio Player</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
        .player { max-width: 500px; margin: 0 auto; }
        audio { width: 100%; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="player">
        <h1>Your Audio</h1>
        <audio controls autoplay>
            <source src="audio.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    </div>
</body>
</html>"""

            with open(os.path.join(server_dir, "index.html"), "w") as f:
                f.write(html_content)

            # Start server
            print("\nStarting HTTP server...")
            print("To access your audio:")
            print("1. Connect your phone to the same WiFi network as this computer")
            print("2. Find this computer's IP address on the network")
            print("3. On your phone, go to: http://<computer-ip>:8000")
            print("\nPress Ctrl+C to stop the server when finished.")

            # Change to server directory and start server
            original_dir = os.getcwd()
            os.chdir(server_dir)

            try:
                # Use Python's built-in HTTP server
                subprocess.run(["python", "-m", "http.server", "8000"])
            except KeyboardInterrupt:
                print("\nServer stopped.")
            finally:
                os.chdir(original_dir)
        else:
            print(f"Error: MP3 file not found at {self.mp3_path}")

if __name__ == "__main__":
    app = AudioStreamingOptions()
    app.show_options()
