# import os
from yt_dlp import YoutubeDL

def download_video(url, output_path="downloads/yt_video.%(ext)s"):
    downloaded_file = None
    
    def post_hook(d):
        nonlocal downloaded_file
        if d['status'] == 'finished':
            downloaded_file = d['filename']
    
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best',
        'noplaylist': True,
        'no_warnings': True,
        'quiet': True,
        'progress_hooks': [post_hook],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)
        return downloaded_file