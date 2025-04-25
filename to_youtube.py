#!/usr/bin/env python3
"""
Script to create an MP4 video from an MP3 audio file and a PNG image.
"""

import os
import argparse
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip

def create_video(image_path, audio_path, output_path=None):
    """
    Create an MP4 video from an audio file and an image.

    Args:
        image_path (str): Path to the PNG image.
        audio_path (str): Path to the MP3 audio file.
        output_path (str, optional): Path to save the output video. If None,
                                     will use the audio filename with .mp4 extension.

    Returns:
        str: Path to the created video file.
    """
    try:
        # Load the audio file
        audio_clip = AudioFileClip(audio_path)

        # Load the image file and set its duration to match the audio
        image_clip = ImageClip(image_path).set_duration(audio_clip.duration)

        # Set the audio of the image clip
        video_clip = image_clip.set_audio(audio_clip)

        # If no output path is specified, derive it from the audio filename
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            output_path = f"{base_name}.mp4"

        # Write the result to a file
        video_clip.write_videofile(output_path, fps=24, codec='libx264',
                                  audio_codec='aac',
                                  temp_audiofile='temp-audio.m4a',
                                  remove_temp=True)

        # Close the clips to free up memory
        video_clip.close()
        audio_clip.close()
        image_clip.close()

        return output_path

    except Exception as e:
        print(f"Error creating video: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Create an MP4 video from an MP3 audio file and a PNG image.')
    parser.add_argument('image', help='Path to the PNG image file')
    parser.add_argument('audio', help='Path to the MP3 audio file')
    parser.add_argument('-o', '--output', help='Path to save the output video')

    args = parser.parse_args()

    # Check if input files exist
    if not os.path.exists(args.image):
        print(f"Error: Image file not found: {args.image}")
        return

    if not os.path.exists(args.audio):
        print(f"Error: Audio file not found: {args.audio}")
        return

    # Create the video
    output_file = create_video(args.image, args.audio, args.output)

    if output_file:
        print(f"Video created successfully: {output_file}")
    else:
        print("Failed to create video.")

if __name__ == "__main__":
    main()
