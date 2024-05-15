import os
from pathlib import Path
from pydub import AudioSegment
from openai import OpenAI
import re

def transcribe_to_file(input_file_path, output_folder_path, model_name="whisper-1", chunk_length_ms=60000):
    # Ensure output folder exists
    output_folder = Path(output_folder_path)
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Load and convert the video file to audio
    video = AudioSegment.from_file(str(input_file_path), format="mp4")
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    temp_audio_path = output_folder / "temp_audio.mp3"
    audio.export(str(temp_audio_path), format="mp3")
    
    # Initialize OpenAI client
    client = OpenAI()

    def chunk_audio(file_path):
        audio = AudioSegment.from_file(str(file_path), format="mp3")
        length_audio = len(audio)
        for i in range(0, length_audio, chunk_length_ms):
            yield audio[i:i+chunk_length_ms]

    def format_timestamp(seconds):
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    json_output = []
    txt_output_path = output_folder / "transcription_output.txt"
    
    start_time = 0
    with txt_output_path.open('w') as txt_file:
        for i, chunk in enumerate(chunk_audio(temp_audio_path)):
            temp_chunk_path = output_folder / f"temp_chunk_{i}.mp3"
            chunk.export(str(temp_chunk_path), format="mp3")

            with open(temp_chunk_path, "rb") as audio_file:
                print(f"Transcribing chunk {i+1}...")
                transcript = client.audio.transcriptions.create(
                    model=model_name, 
                    file=audio_file
                )

            temp_chunk_path.unlink()  # Remove temp chunk file
            
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', transcript.text)
            chunk_duration = len(chunk) / 1000  # Duration in seconds
            sentence_duration = chunk_duration / len(sentences)

            for sentence in sentences:
                timestamp = format_timestamp(start_time)
                txt_file.write(f"{timestamp} {sentence}\n")
                json_output.append({"timestamp": timestamp, "text": sentence})
                start_time += sentence_duration
    
    # Export JSON transcription
    json_output_path = output_folder / "transcription_output.json"
    with json_output_path.open('w') as json_file:
        import json
        json.dump(json_output, json_file, indent=4)
    
    # Clean up temp audio file
    temp_audio_path.unlink()
