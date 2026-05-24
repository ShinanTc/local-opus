from typing import List, Dict
from transcript.get_candidate_segments import get_candidate_segments
from transcript.score_candidate_segments import score_candidate_segments
from transcript.select_top_segments import select_top_segments


def extract_highlights(
    transcript_path: str = "transcription.txt",
    niche: str = "travel",
) -> List[Dict]:
    """
    Extracts key highlight segments from a speech/narration transcript.

    Designed for podcast and TED-talk style videos only.
    Skips intros, outros, and filler — returns high-value insight moments
    distributed across the video, ready for reel extraction.

    Steps:
      1. Parse transcript into candidate segments.
      2. Batch-score segments for insight quality via AI.
      3. Select top diverse segments with temporal spacing enforced.
    """
    candidate_segments = get_candidate_segments(transcript_path)

    scored_segments = score_candidate_segments(
        candidate_segments=candidate_segments,
        niche=niche,
    )

    return select_top_segments(scored_segments=scored_segments)