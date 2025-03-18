import whisper

def transcribe_audio_whisper(filename):
    model = whisper.load_model("small")  # Adjust model size if needed
    result = model.transcribe(filename)
    return result["text"]
