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
        "-y",  # overwrite output if exists
        "-i",
        video_path,
        "-ss",
        f"{start:.3f}",  # precise start
        "-t",
        f"{duration:.3f}",  # exact duration
        "-map",
        "0:v:0",  # map first video stream
        "-map",
        "0:a?",  # map first audio stream if exists
        "-c:v",
        "libx264",  # CPU-friendly codec
        "-preset",
        "veryfast",  # balance speed vs quality
        "-crf",
        "18",  # visually lossless
        "-c:a",
        "aac",  # audio codec
        "-movflags",
        "+faststart",
        output_path,
    ]

    subprocess.run(cmd, check=True)
