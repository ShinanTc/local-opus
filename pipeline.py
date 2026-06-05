import os
import time
from io_modules.transcribe_video import transcribe_video
from services.extract_highlights import extract_highlights
from services.video.extract_all_raw_clips import extract_all_raw_clips
from services.video.collect_slide_timestamps import collect_slide_timestamps
from services.video.apply_slide_fills import apply_slide_fills


def _fmt(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m}m {s}s" if m else f"{s}s"


def run_pipeline():
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
    pipeline_start = time.time()

    t = time.time()
    transcribe_video()
    print(f"✅ Transcription successful ({_fmt(time.time() - t)})", flush=True)

    print("Step 3: Finding highlights...", flush=True)
    t = time.time()
    highlights = extract_highlights(niche=niche)
    print(f"✅ Highlights extracted! ({_fmt(time.time() - t)})", flush=True)

    print("Step 4: Extracting raw video clips...", flush=True)
    raw_dir = os.path.abspath("raw_clips")
    t = time.time()
    clip_paths = extract_all_raw_clips(
        video_path=video_path, highlights=highlights, out_dir=raw_dir
    )
    print(f"✅ Extracted {len(clip_paths)} raw clips ({_fmt(time.time() - t)})", flush=True)

    print("Step 5: Collecting slide timestamps...", flush=True)
    t = time.time()
    slide_map = collect_slide_timestamps(clip_paths)
    print(f"✅ Slide timestamps collected! ({_fmt(time.time() - t)})", flush=True)

    print("Step 6: Cropping to 9:16 and applying slide fills...", flush=True)
    final_dir = os.path.abspath("final_clips")
    t = time.time()
    final_paths = apply_slide_fills(clip_paths, slide_map, final_dir)
    print(f"✅ {len(final_paths)} final clips saved to {final_dir} ({_fmt(time.time() - t)})", flush=True)

    print(f"\n⏱  Total pipeline time: {_fmt(time.time() - pipeline_start)}", flush=True)