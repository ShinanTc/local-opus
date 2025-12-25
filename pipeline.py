from youtube_downloader import download_video

def run_pipeline():
    """
    This is the main execution pipeline.
    Each step (download, transcription, highlights) will be added here.
    """
    video_url = input("Enter YouTube video URL: ")

    print("Step 1: Downloading video...")
    download_video(video_url)
    print("Video downloaded successfully!")

    # Future steps:
    # print("Step 2: Transcribing video...")
    # transcribe_video(...)
    
    # print("Step 3: Finding highlights...")
    # extract_highlights(...)
