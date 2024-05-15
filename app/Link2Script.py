from pytube import YouTube
from pathlib import Path
from autotranscribe import transcribe_to_file

def download_youtube_video(url, path='./'):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
        # Specify the output filename directly
        stream.download(output_path=path, filename='temp')
        return 'temp.mp4'  # Return the fixed filename
    except Exception as e:
        raise Exception(f"Failed to download video: {e}")
    

def URL2Script(youtube_url, output_folder_path):
    try:
        print("Downloading the video...")
        video_filename = download_youtube_video(youtube_url, output_folder_path)
        video_file_path = Path(output_folder_path) / video_filename
        
        print("Transcribing the video...")
        transcribe_to_file(str(video_file_path), output_folder_path)
        
        print("Cleaning up temporary files...")
        video_file_path.unlink()  # Remove the downloaded MP4 file
        
        temp_audio_path = Path(output_folder_path) / "temp_audio.mp3"
        if temp_audio_path.exists():
            temp_audio_path.unlink()
            
        print("Transcription complete. Output files saved.")
    except Exception as e:
        print(f"An error occurred during processing: {e}")
    
    