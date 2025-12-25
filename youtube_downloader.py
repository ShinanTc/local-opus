from yt_dlp import YoutubeDL

def download_video(url, output_path="downloads/%(title)s.%(ext)s"):
    """
    Downloads a single YouTube video from the provided URL.
    """
    ydl_opts = {
        'outtmpl': output_path,  # Save location and file name template
        'format': 'best',        # Download best quality
        'noplaylist': True       # Only download a single video
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
