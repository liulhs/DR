from pytube import YouTube
from pathlib import Path
import re
from autotranscribe import transcribe_to_file

def sanitize_filename(title):
    # Remove any invalid characters from the title
    return re.sub(r'[\\/*?:"<>|]', "", title)

def download_youtube_video(url, path='./'):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
        title = sanitize_filename(yt.title)
        filename = f"{title}.mp4"
        # Specify the output filename directly
        stream.download(output_path=path, filename=filename)
        return filename  # Return the sanitized title as the filename
    except Exception as e:
        raise Exception(f"Failed to download video: {e}")

def URL2Script(youtube_url, output_folder_path):
    try:
        print("Downloading the video...")
        video_filename = download_youtube_video(youtube_url, output_folder_path)
        video_file_path = Path(output_folder_path) / video_filename
        video_title = video_filename.rsplit('.', 1)[0]  # Remove the file extension
        
        print("Transcribing the video...")
        transcribe_to_file(str(video_file_path), output_folder_path, output_name=video_title)
        
        print("Cleaning up temporary files...")
        video_file_path.unlink()  # Remove the downloaded MP4 file
        
        temp_audio_path = Path(output_folder_path) / "temp_audio.mp3"
        if temp_audio_path.exists():
            temp_audio_path.unlink()
            
        print("Transcription complete. Output files saved.")
        return video_title  # Return the video title for further use
    except Exception as e:
        print(f"An error occurred during processing: {e}")
        return None