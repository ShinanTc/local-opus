from faster_whisper import WhisperModel
import os
import json


def transcribe_video(
    video_path: str = "downloads/yt_video.mp4",
    output_file: str = "transcription.txt",
    model_size: str = "small"
):
    """
    Transcribes a video using faster-whisper and saves:
      - transcription.txt  : human-readable [start --> end] segments
      - transcription.json : full word-level timestamps for karaoke subtitles

    Uses word-level timestamps to get the true start of speech per segment,
    avoiding Whisper's known behavior of anchoring the first segment to 0.0.
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
        language="en",
        word_timestamps=True
    )

    json_output_file = os.path.splitext(output_file)[0] + ".json"
    segment_data = []

    with open(output_file, "w", encoding="utf-8") as f:
        for segment in segments:
            if segment.words:
                start = round(segment.words[0].start, 2)
                end   = round(segment.words[-1].end, 2)
            else:
                start = round(segment.start, 2)
                end   = round(segment.end, 2)

            text = segment.text.strip()
            f.write(f"[{start} --> {end}] {text}\n")

            # Build word list — fall back gracefully if words are missing
            words = []
            if segment.words:
                for w in segment.words:
                    words.append({
                        "word":  w.word.strip(),
                        "start": round(w.start, 3),
                        "end":   round(w.end,   3),
                    })

            segment_data.append({
                "start": start,
                "end":   end,
                "text":  text,
                "words": words,
            })

    with open(json_output_file, "w", encoding="utf-8") as jf:
        json.dump(segment_data, jf, indent=2, ensure_ascii=False)

    print(f"✅ Transcription saved to {output_file}")
    print(f"✅ Word-level JSON saved to {json_output_file}")