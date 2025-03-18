from flask import Flask, render_template, request, redirect, url_for
import os
import yt_dlp
import whisper
from pydub import AudioSegment

app = Flask(__name__)

# Function to download audio from YouTube
def download_audio(youtube_link, output_file="downloaded_audio.wav"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_link])
    if os.path.exists("downloaded_audio.wav"):
        os.rename("downloaded_audio.wav", output_file)

# Function to split audio into chunks
def split_audio(input_file, chunk_length_ms=30000):
    audio = AudioSegment.from_file(input_file)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_file = f"chunk_{i // chunk_length_ms}.wav"
        chunk.export(chunk_file, format="wav")
        chunks.append(chunk_file)
    return chunks

# Function to transcribe audio using Whisper
def transcribe_audio_whisper(filename):
    model = whisper.load_model("small")  # You can change model size if needed
    result = model.transcribe(filename)
    return result["text"]

# Function to process transcription
def process_transcription(youtube_link):
    download_path = "downloaded_audio.wav"
    print("Downloading audio...")
    download_audio(youtube_link, download_path)
    print("Audio downloaded!")

    print("Splitting audio into chunks...")
    audio_chunks = split_audio(download_path)
    print("Audio processing completed!")

    full_transcription = ""
    for i, chunk in enumerate(audio_chunks, 1):
        print(f"Transcribing part {i} of {len(audio_chunks)}...")
        transcription = transcribe_audio_whisper(chunk)
        full_transcription += transcription + "\n"
        os.remove(chunk)
    
    if os.path.exists(download_path):
        os.remove(download_path)

    
    print("---------------------------------------------------- TRANSCRIPTION ---------------------------------------------------------")
    print(full_transcription)
    print("---------------------------------------------------Transcription completed!-------------------------------------------------")
    return full_transcription

# Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# Get Started Page: User enters the YouTube link
@app.route('/get-started', methods=['GET', 'POST'])
def get_started():
    if request.method == 'POST':
        youtube_link = request.form.get('youtube_link')
        transcription = process_transcription(youtube_link)
        return redirect(url_for('show_transcription', transcription=transcription))
    return render_template('get_started.html')

# Transcription Display Page
@app.route('/transcription')
def show_transcription():
    transcription = request.args.get('transcription', '')
    return f"<h2>Transcription:</h2><p>{transcription}</p>"

if __name__ == '__main__':
    app.run(debug=True)