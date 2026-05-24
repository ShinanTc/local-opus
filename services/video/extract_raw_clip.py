import subprocess

def extract_raw_clip(
    video_path: str, output_path: str, start: float, end: float
) -> None:
    """
    Deterministically extracts a single raw clip from a video using FFmpeg.
    Args:
        video_path (str): Path to the source video.
        output_path (str): Path to save the extracted clip.
        start (float): Start timestamp in seconds.
        end (float): End timestamp in seconds.
    Behavior:
        - No padding or trimming applied.
        - Re-encodes video and audio for frame-accurate extraction.
        - Deterministic output length: end - start.
    """
    duration = max(0.0, end - start)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-ss",
        f"{start:.3f}",
        "-t",
        f"{duration:.3f}",
        "-map",
        "0:v:0",
        "-map",
        "0:a?",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg failed with code {result.returncode}\n"
            f"CMD: {' '.join(cmd)}\n"
            f"STDERR:\n{result.stderr}"
        )