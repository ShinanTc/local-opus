from typing import List, Dict
from get_candidate_segments import get_candidate_segments

def extract_highlights(transcript_path: str = "transcription.txt") -> List[Dict]:
    """
    Public method to extract candidate highlight segments from a transcript.
    """
    candidate_segments = get_candidate_segments(transcript_path)

    return candidate_segments
