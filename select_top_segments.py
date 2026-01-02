from typing import List, Dict


def select_top_segments(
    scored_segments: List[Dict],
    top_k: int = 5,
    min_final_score: float = 0.0,
) -> List[Dict]:
    """
    Selects the best highlight candidates purely based on final_score.

    No ordering, no gap checks, no AI.
    """

    if not scored_segments:
        return []

    # Filter by minimum score if needed
    filtered = [
        seg for seg in scored_segments
        if seg.get("final_score", 0) >= min_final_score
    ]

    # Sort by final_score (descending)
    filtered.sort(key=lambda x: x.get("final_score", 0), reverse=True)

    # Pick top K
    return filtered[:top_k]
