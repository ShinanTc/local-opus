from typing import List, Dict
from get_candidate_segments import get_candidate_segments
from score_candidate_segments import score_candidate_segments
# import json


def extract_highlights(
    transcript_path: str = "transcription.txt",
    niche: str = "travel",
) -> List[Dict]:
    """
    Public method to extract scored highlight segments from a transcript.
    """

    # Step 1 + 2: structural + semantic segmentation
    candidate_segments = get_candidate_segments(transcript_path)

    # print("CANDIDATE SEGMENTS ------------------------ ✅")
    # print(json.dumps(candidate_segments, indent=2, sort_keys=True))

    # Step 3: intent-based scoring
    scored_segments = score_candidate_segments(
        candidate_segments=candidate_segments,
        niche=niche,
    )

    # print("SEGMENT SCORING COMPLETED ------------------------ ✅")
    # print(json.dumps(scored_segments, indent=2, sort_keys=True))

    return scored_segments
