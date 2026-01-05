from io_modules.youtube_downloader import download_video
from io_modules.transcribe_video import transcribe_video
from services.extract_highlights import extract_highlights

def run_pipeline():
    """
    This is the main execution pipeline.
    Each step (download, transcription, highlights) will be added here.
    """
    video_url = input("Enter YouTube video URL: ")
    niche = input(
        "What niche should the highlights focus on? "
        "(e.g., travel, fitness, business, education): "
    )

    print("⬇️  Downloading video...")
    download_video(video_url)
    print("✅ Video downloaded successfully!")

    transcribe_video()
    print("✅ Transcription successfull")
    
    print("Step 3: Finding highlights...")
    extract_highlights(niche=niche)
