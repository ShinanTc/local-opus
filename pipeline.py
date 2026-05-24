import os
from io_modules.transcribe_video import transcribe_video
from services.extract_highlights import extract_highlights
from services.video.extract_all_raw_clips import extract_all_raw_clips

def run_pipeline():
    """
    Main execution pipeline:
    1. Download (skipped for now)
    2. Transcribe
    3. Highlight extraction
    4. Video clip extraction
    """
    niche = input(
        "What niche should the highlights focus on? "
        "(e.g., travel, fitness, business, education): "
    )

    # Hardcoded for testing — skip download step
    video_path = os.path.abspath("downloads/yt_video.mp4")
    if not os.path.exists(video_path):
        raise FileNotFoundError(
            f"Video file not found at: {video_path}\n"
            f"Files in that folder: {os.listdir(os.path.dirname(video_path))}"
        )
    print(f"✅ Using existing video: {video_path}", flush=True)

    transcribe_video()
    print("✅ Transcription successful", flush=True)

    print("Step 3: Finding highlights...", flush=True)
    highlights = extract_highlights(niche=niche)
    print("✅ Highlights extracted!", flush=True)

    print("Step 4: Extracting raw video clips...", flush=True)
    output_dir = os.path.abspath("raw_clips")
    clip_paths = extract_all_raw_clips(
        video_path=video_path, highlights=highlights, out_dir=output_dir
    )
    print(f"✅ Extracted {len(clip_paths)} raw clips to {output_dir}", flush=True)