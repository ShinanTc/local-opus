from io_modules.youtube_downloader import download_video
from io_modules.transcribe_video import transcribe_video
from services.extract_highlights import extract_highlights
from services.video.extract_all_raw_clips import extract_all_raw_clips

def run_pipeline():
    """
    Main execution pipeline:
    1. Download
    2. Transcribe
    3. Highlight extraction
    4. Video clip extraction
    """
    video_url = input("Enter YouTube video URL: ")
    niche = input(
        "What niche should the highlights focus on? "
        "(e.g., travel, fitness, business, education): "
    )

    print("⬇️  Downloading video...")
    video_path = download_video(video_url)
    print("✅ Video downloaded successfully!")

    transcribe_video()
    print("✅ Transcription successful")

    print("Step 3: Finding highlights...")
    highlights = extract_highlights(niche=niche)
    print("✅ Highlights extracted!")

    print("Step 4: Extracting raw video clips...")
    
    output_dir = "raw_clips"
    clip_paths = extract_all_raw_clips(video_path=video_path, highlights=highlights, out_dir=output_dir)

    print(f"✅ Extracted {len(clip_paths)} raw clips to {output_dir}")
