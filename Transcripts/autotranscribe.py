import json
from pydub import AudioSegment
import whisper
from pathlib import Path

def transcribe_to_json_and_txt(mp4_file_path, json_output_path, txt_output_path, chunk_length_ms=60000):
    # Load the video file and convert it to audio
    video = AudioSegment.from_file(mp4_file_path, format="mp4")
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio.export("audio.mp3", format="mp3")

    # Define helper functions
    def chunk_audio(file_path, chunk_length_ms=60000):
        audio = AudioSegment.from_file(file_path, format="mp3")
        length_audio = len(audio)
        chunks = []
        for i in range(0, length_audio, chunk_length_ms):
            chunks.append(audio[i:i+chunk_length_ms])
        return chunks

    def format_timestamp(seconds):
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"[{hours:02d}:{minutes:02d}:{seconds:02d}]"

    def transcribe_chunk(chunk, model, start_time):
        temp_file = Path("temp_chunk.mp3")
        chunk.export(temp_file, format="mp3")
        result = model.transcribe(temp_file)
        temp_file.unlink()  # Removes the file

        transcriptions = []
        for segment in result['segments']:
            timestamp = format_timestamp(start_time + segment['start'])
            transcriptions.append(f"{timestamp} {segment['text']}")

        return '\n'.join(transcriptions), start_time + result['duration']

    def transcribe_audio(file_path, chunk_length_ms=60000):
        model = whisper.load_model("base")  # or any other model size
        audio_chunks = chunk_audio(file_path, chunk_length_ms)

        file_path = Path(file_path)
        output_file = file_path.parent / "transcription_output.txt"

        start_time = 0
        with output_file.open('w') as f:
            for i, chunk in enumerate(audio_chunks):
                try:
                    print(f"Transcribing chunk {i+1}/{len(audio_chunks)}...")
                    transcription, start_time = transcribe_chunk(chunk, model, start_time)
                    f.write(transcription + '\n')
                except Exception as e:
                    print(f"Error transcribing chunk {i+1}: {e}")

    # Transcribe audio and save to JSON and TXT
    transcribe_audio("audio.mp3", chunk_length_ms)

    # Save transcription to JSON
    with open(json_output_path, 'w') as json_file:
        json.dump({"transcription": "transcription_output.txt"}, json_file)

    # Copy TXT transcription to specified output path
    txt_output_path = Path(txt_output_path)
    output_txt_path = txt_output_path.parent / "transcription_output.txt"
    output_txt_path.rename(txt_output_path)

# Usage example
transcribe_to_json_and_txt("F:\Study\Github_Repos\DR\Transcripts\Discussion_Week8.mp4", "output/transcription.json", "output/transcription.txt")
