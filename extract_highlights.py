from typing import List, Dict
from get_candidate_segments import get_candidate_segments
from score_candidate_segments import score_candidate_segments
from select_top_segments import select_top_segments
from compute_segment_gaps import compute_segment_gaps
from identify_gap_risks import identify_gap_risks
from handle_gap_risks import handle_gap_risks
from verify_continuity_with_ai import verify_continuity_with_ai
import json

MAX_HIGHLIGHT_DURATION = 60  # seconds, adjustable

def merge_continuous_segments(segments: List[Dict]) -> List[Dict]:
    """
    Merge adjacent verified segments into longer highlights if:
      - ai_continuous == True
      - gap_from_previous == 1 (no risky gap)
      - combined duration <= MAX_HIGHLIGHT_DURATION
    """
    if not segments:
        return []

    merged_segments = []
    buffer = segments[0].copy()

    for seg in segments[1:]:
        can_merge = (
            seg.get('ai_continuous', False)
            and seg.get('gap_from_previous', 1) == 1
            and (buffer['end'] - buffer['start'] + seg['end'] - seg['start']) <= MAX_HIGHLIGHT_DURATION
        )
        if can_merge:
            buffer['end'] = seg['end']
            buffer['text'] += " " + seg['text']
            buffer['lines'].extend(seg['lines'])
        else:
            merged_segments.append(buffer)
            buffer = seg.copy()
    merged_segments.append(buffer)
    return merged_segments

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

    # Step 8: Verify continuity with AI
    verified_segments = verify_continuity_with_ai(handled_segments)

    # Step 9: Merge continuous verified segments
    merged_segments = merge_continuous_segments(verified_segments)

    print("MERGED HIGHLIGHT SEGMENTS ------------------------ ✅")
    print(json.dumps(merged_segments, indent=2, sort_keys=True))

    return merged_segments
