from typing import List, Dict

def buffers_to_candidate_segments(buffers: List[List[Dict]]) -> List[Dict]:
    """
    Converts buffers into indexed candidate segments.
    """
    segments = []

    for index, buffer in enumerate(buffers):
        segments.append({
            "index": index,
            "start": buffer[0]["start"],
            "end": buffer[-1]["end"],
            "text": " ".join(l["text"] for l in buffer),
            "lines": buffer.copy(),
        })

    return segments
