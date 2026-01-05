from typing import List, Dict
from services.ai_constraints import ai_should_close_buffer

def build_buffers(
    lines: List[Dict],
    max_segment_duration: float,
    max_lines_per_segment: int,
) -> List[List[Dict]]:
    """
    Groups transcript lines into semantic buffers using hard + AI constraints.
    """
    buffers = []
    buffer: List[Dict] = []

    for line in lines:
        if not buffer:
            buffer.append(line)
            continue

        buffer_text = " ".join(l["text"] for l in buffer)
        current_duration = line["end"] - buffer[0]["start"]

        within_duration = current_duration <= max_segment_duration
        within_line_limit = len(buffer) < max_lines_per_segment
        ai_close = ai_should_close_buffer(buffer_text, line["text"])

        if within_duration and within_line_limit and not ai_close:
            buffer.append(line)
        else:
            buffers.append(buffer)
            buffer = [line]

    if buffer:
        buffers.append(buffer)

    return buffers
