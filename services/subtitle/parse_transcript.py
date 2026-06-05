import json
import os
from typing import List, Dict


def parse_transcript(transcript_json: str = "transcription.json") -> List[Dict]:
    """
    Loads transcription.json produced by transcribe_video() and returns
    a list of segments, each with word-level timestamps.

    Returns:
        [
            {
                "start": 20.62,
                "end":   26.7,
                "text":  "So the idea that I want to share...",
                "words": [
                    {"word": "So",  "start": 20.62, "end": 20.91},
                    {"word": "the", "start": 20.91, "end": 21.04},
                    ...
                ]
            },
            ...
        ]
    """
    if not os.path.exists(transcript_json):
        raise FileNotFoundError(
            f"Transcript JSON not found: {transcript_json}\n"
            f"Make sure transcribe_video() has been run with word_timestamps=True."
        )

    with open(transcript_json, "r", encoding="utf-8") as f:
        segments = json.load(f)

    # Validate structure minimally
    for i, seg in enumerate(segments):
        if "words" not in seg or "start" not in seg or "end" not in seg:
            raise ValueError(
                f"Segment {i} is missing required keys (start/end/words). "
                f"Re-run transcribe_video() to regenerate the JSON."
            )

    return segments