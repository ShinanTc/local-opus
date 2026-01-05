import re
from typing import List, Dict

LINE_PATTERN = re.compile(r"\[(\d+\.?\d*)\s*-->\s*(\d+\.?\d*)\]\s*(.+)")

def parse_transcript_file(transcript_path: str) -> List[Dict]:
    """
    Parses a Whisper-style transcript file into structured lines.
    """
    lines = []

    with open(transcript_path, "r", encoding="utf-8") as f:
        for raw in f:
            match = LINE_PATTERN.match(raw.strip())
            if not match:
                continue

            start, end, text = match.groups()
            lines.append({
                "start": float(start),
                "end": float(end),
                "text": text.strip(),
            })

    return lines
