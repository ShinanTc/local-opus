import os
from typing import List, Dict
from services.video.extract_raw_clip import extract_raw_clip

def extract_all_raw_clips(
    video_path: str,
    highlights: List[Dict],
    out_dir: str
) -> List[str]:
    """
    Batch extracts multiple raw clips based on highlight segments.

    Args:
        video_path (str): Path to the source video.
        highlights (List[Dict]): List of highlights with 'start' and 'end'.
        out_dir (str): Directory to save all clips.

    Returns:
        List[str]: List of paths to extracted clips.

    Behavior:
        - Uses deterministic filenames: "{start_ms}_{end_ms}.mp4"
        - Calls `extract_raw_clip` for each highlight.
    """
    video_path = os.path.abspath(video_path)
    out_dir = os.path.abspath(out_dir)

    os.makedirs(out_dir, exist_ok=True)
    clip_paths = []

    print("Right before for loop")

    for h in highlights:
        start_ms = int(h["start"] * 1000)
        end_ms = int(h["end"] * 1000)
        filename = f"{start_ms}_{end_ms}.mp4"

        output_path = os.path.join(out_dir, filename)

        extract_raw_clip(
            video_path=video_path,
            output_path=output_path,
            start=h["start"],
            end=h["end"]
        )

        clip_paths.append(output_path)

    print("After for loop")

    return clip_paths