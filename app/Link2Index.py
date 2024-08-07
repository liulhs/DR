from Link2Script import URL2Script
from transcript_embed import create_index
from pathlib import Path


def URL2Index(youtube_url, output_folder_path, index_folder, model_name="BAAI/bge-m3"):
    video_title = URL2Script(youtube_url, output_folder_path)
    if video_title:
        txt_file_path = Path(output_folder_path) / f"{video_title}.txt"
        create_index(str(txt_file_path), index_folder, youtube_url, model_name)
        print("Index creation complete.")
    else:
        print("Failed to download and transcribe video. Index creation aborted.")