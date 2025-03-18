import os
import yt_dlp

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
