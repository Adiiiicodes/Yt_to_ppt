import os
from download_audio import download_audio
from split_audio import split_audio
from transcribe_audio import transcribe_audio_whisper

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

    #print("---------------------------------------------------- TRANSCRIPTION ---------------------------------------------------------")
    #print(full_transcription)
    #print("------------------------------------------------ Transcription completed! ------------------------------------------------")
    return full_transcription
