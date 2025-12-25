from youtube_downloader import download_video
from transcribe_video import transcribe_video

def run_pipeline():
    """
    This is the main execution pipeline.
    Each step (download, transcription, highlights) will be added here.
    """
    video_url = input("Enter YouTube video URL: ")

    print("⬇️  Downloading video...")
    download_video(video_url)
    print("✅ Video downloaded successfully!")

    # Future steps:
    transcribe_video()
    print("✅ Transcription successfull")

    
    # print("Step 3: Finding highlights...")
    # extract_highlights(...)
