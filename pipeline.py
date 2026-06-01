import os
from io_modules.transcribe_video import transcribe_video
from services.extract_highlights import extract_highlights
from services.video.extract_all_raw_clips import extract_all_raw_clips
from services.video.reformat_all_clips import reformat_all_clips


def run_pipeline():
    """
    Main execution pipeline:
    1. Download (skipped for now)
    2. Transcribe
    3. Highlight extraction
    4. Raw video clip extraction
    5. Hard crop to 9:16 vertical
    """
    niche = input(
        "What niche should the highlights focus on? "
        "(e.g., travel, fitness, business, education): "
    )

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
    raw_dir = os.path.abspath("raw_clips")
    clip_paths = extract_all_raw_clips(
        video_path=video_path, highlights=highlights, out_dir=raw_dir
    )
    print(f"✅ Extracted {len(clip_paths)} raw clips", flush=True)

    print("Step 5: Cropping clips to vertical 9:16...", flush=True)
    vertical_dir = os.path.abspath("vertical_clips")
    vertical_paths = reformat_all_clips(
        clip_paths=clip_paths,
        out_dir=vertical_dir,
    )
    print(f"✅ {len(vertical_paths)} vertical clips saved to {vertical_dir}", flush=True)