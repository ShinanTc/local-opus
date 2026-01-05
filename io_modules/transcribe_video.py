from faster_whisper import WhisperModel
import os

def transcribe_video(
    video_path: str = "downloads/yt_video.mp4",
    output_file: str = "transcription.txt",
    model_size: str = "small"
):
    """
    Transcribes a video using faster-whisper and saves the output to a file.
    """

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    print("🦻  Loading Whisper model...")
    model = WhisperModel(
        model_size,
        device="cpu",
        compute_type="int8"
    )

    print("✍️  Transcribing video...")
    segments, info = model.transcribe(
        video_path,
        beam_size=5,
        language="en"          # remove if auto-detection is needed
    )

    with open(output_file, "w", encoding="utf-8") as f:
        for segment in segments:
            start = round(segment.start, 2)
            end = round(segment.end, 2)
            text = segment.text.strip()

            f.write(f"[{start} --> {end}] {text}\n")

    print(f"Transcription saved to {output_file}")
