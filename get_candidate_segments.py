import re
from typing import List, Dict
from services.ai_constraints import ai_should_close_buffer

def get_candidate_segments(
    transcript_path: str = "transcription.txt",
    max_segment_duration: float = 12.0,
    max_lines_per_segment: int = 4,
) -> List[Dict]:
    """
    Groups transcript lines into candidate segments with AI semantic checking.
    """
    line_pattern = re.compile(r"\[(\d+\.?\d*)\s*-->\s*(\d+\.?\d*)\]\s*(.+)")
    lines = []

    # Parse transcript
    with open(transcript_path, "r", encoding="utf-8") as f:
        for raw in f:
            match = line_pattern.match(raw.strip())
            if not match:
                continue
            start, end, text = match.groups()
            lines.append({
                "start": float(start),
                "end": float(end),
                "text": text.strip()
            })

    segments = []
    buffer = []

    for line in lines:
        if not buffer:
            buffer.append(line)
            continue

        buffer_text = " ".join(l["text"] for l in buffer)
        current_duration = line["end"] - buffer[0]["start"]

        # Hard constraints
        within_duration = current_duration <= max_segment_duration
        within_line_limit = len(buffer) < max_lines_per_segment

        # AI constraint
        ai_close = ai_should_close_buffer(buffer_text, line["text"])

        if within_duration and within_line_limit and not ai_close:
            buffer.append(line)
        else:
            segments.append({
                "start": buffer[0]["start"],
                "end": buffer[-1]["end"],
                "text": buffer_text,
                "lines": buffer.copy()
            })
            buffer = [line]

    # Flush remaining buffer
    if buffer:
        segments.append({
            "start": buffer[0]["start"],
            "end": buffer[-1]["end"],
            "text": " ".join(l["text"] for l in buffer),
            "lines": buffer.copy()
        })

    return segments
