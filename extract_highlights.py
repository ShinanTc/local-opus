from typing import List, Dict
from get_candidate_segments import get_candidate_segments
from score_candidate_segments import score_candidate_segments
from select_top_segments import select_top_segments
from compute_segment_gaps import compute_segment_gaps
import json


def extract_highlights(
    transcript_path: str = "transcription.txt",
    niche: str = "travel",
) -> List[Dict]:
    """
    Public method to extract highlight segments from a transcript.
    """

    # Step 1 + 2: line → buffer → candidate segments
    candidate_segments = get_candidate_segments(transcript_path)

    # Step 3: score each candidate
    scored_segments = score_candidate_segments(
        candidate_segments=candidate_segments,
        niche=niche,
    )

    # Step 4: select best segments purely by score
    selected_segments = select_top_segments(
        scored_segments=scored_segments,
    )
    
    computed_gaps = compute_segment_gaps(selected_segments)
    
    print("COMPUTED GAPS ------------------------ ✅")
    print(json.dumps(computed_gaps, indent=2, sort_keys=True))

    return selected_segments