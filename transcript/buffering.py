from typing import List, Dict
from services.ai_constraints import ai_should_close_buffer

MIN_SEGMENT_DURATION = 30.0


def _is_sentence_boundary(text: str) -> bool:
    """
    Returns True if the text ends with sentence-closing punctuation,
    meaning the NEXT line is a clean thought start.
    """
    return text.strip().endswith((".", "?", "!"))


def build_buffers(
    lines: List[Dict],
    max_segment_duration: float,
    max_lines_per_segment: int,
) -> List[List[Dict]]:
    """
    Groups transcript lines into semantic buffers using hard + AI constraints.

    A buffer is only closed when ALL of these are true:
      - Current duration has reached MIN_SEGMENT_DURATION (30s floor)
      - The last line ends at a sentence boundary (clean start for next buffer)
      - Either max duration/lines exceeded OR AI signals a topic close
    """
    buffers = []
    buffer: List[Dict] = []

    for line in lines:
        if not buffer:
            buffer.append(line)
            continue

        current_duration = line["end"] - buffer[0]["start"]
        has_min_duration = current_duration >= MIN_SEGMENT_DURATION
        at_sentence_boundary = _is_sentence_boundary(buffer[-1]["text"])

        # Never close before minimum duration — absorb the line and continue
        if not has_min_duration:
            buffer.append(line)
            continue

        # Past minimum: check hard limits and AI signal
        exceeded_duration = current_duration > max_segment_duration
        exceeded_lines = len(buffer) >= max_lines_per_segment
        buffer_text = " ".join(l["text"] for l in buffer)
        ai_close = ai_should_close_buffer(buffer_text, line["text"])

        should_close = (exceeded_duration or exceeded_lines or ai_close)

        if should_close and at_sentence_boundary:
            buffers.append(buffer)
            buffer = [line]
        else:
            buffer.append(line)

    if buffer:
        buffers.append(buffer)

    return buffers