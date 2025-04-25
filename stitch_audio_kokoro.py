from pydub import AudioSegment
import os

def combine_audio_files(input_dir="output_audio", output_file="output_audio/combined_output.mp3",
                        format="mp3", remove_source_files=True):
    """
    Combines multiple WAV files in numerical order into a single file.

    Args:
        input_dir (str): Directory containing the WAV files
        output_file (str): Name of the output file
        format (str): Output format (mp3, wav, etc.)
        remove_source_files (bool): Whether to remove source WAV files after combining
    """
    # Get all wav files in the directory
    files = [f for f in os.listdir(input_dir) if f.endswith('.wav')]

    # Extract numbers from filenames and sort numerically
    files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    print(f"Found {len(files)} files to combine.")

    # Initialize with the first file
    if not files:
        print("No WAV files found!")
        return

    combined = AudioSegment.from_wav(os.path.join(input_dir, files[0]))
    print(f"Starting with {files[0]}")

    # Append each subsequent file
    for file in files[1:]:
        print(f"Adding {file}")
        audio = AudioSegment.from_wav(os.path.join(input_dir, file))
        combined += audio

    # Export combined audio in the specified format
    combined.export(output_file, format=format)
    print(f"Combined audio saved to {output_file}")

    # Remove source WAV files if requested
    if remove_source_files:
        print("Removing source WAV files...")
        for file in files:
            file_path = os.path.join(input_dir, file)
            try:
                os.remove(file_path)
                print(f"Removed {file}")
            except Exception as e:
                print(f"Error removing {file}: {e}")

if __name__ == "__main__":
    # For MP3 output with WAV file cleanup
    combine_audio_files(output_file="output_audio/combined_output.mp3", format="mp3", remove_source_files=True)
