from typing import List, Dict
from transcript.parsing import parse_transcript_file
from transcript.buffering import build_buffers
from transcript.segments import buffers_to_candidate_segments

def get_candidate_segments(
    transcript_path: str = "transcription.txt",
    max_segment_duration: float = 60.0,
    max_lines_per_segment: int = 20,
) -> List[Dict]:
    """
    High-level pipeline: transcript → buffers → candidate segments.
    """
    lines = parse_transcript_file(transcript_path)
    buffers = build_buffers(
        lines,
        max_segment_duration=max_segment_duration,
        max_lines_per_segment=max_lines_per_segment,
    )
    return buffers_to_candidate_segments(buffers)