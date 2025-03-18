from pydub import AudioSegment

def split_audio(input_file, chunk_length_ms=30000):
    audio = AudioSegment.from_file(input_file)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_file = f"chunk_{i // chunk_length_ms}.wav"
        chunk.export(chunk_file, format="wav")
        chunks.append(chunk_file)
    return chunks
