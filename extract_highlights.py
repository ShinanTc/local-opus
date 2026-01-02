from typing import List, Dict
from get_candidate_segments import get_candidate_segments
from score_candidate_segments import score_candidate_segments
from select_top_segments import select_top_segments
from compute_segment_gaps import compute_segment_gaps
from identify_gap_risks import identify_gap_risks
from handle_gap_risks import handle_gap_risks
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
    
    # Step 5: compute gaps between adjacent segments
    computed_gaps = compute_segment_gaps(selected_segments)

    # Step 6: identify gap risks
    flagged_segments = identify_gap_risks(computed_gaps)

    # Step 7: Handle gap risks
    handled_segments = handle_gap_risks(flagged_segments)

    print("HANDLED SEGMENTS ------------------------ ✅")
    print(json.dumps(handled_segments, indent=2, sort_keys=True))

    return handled_segments