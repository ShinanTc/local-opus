from typing import List, Dict

MAX_HIGHLIGHTS = 6
MIN_GAP_SECONDS = 45.0
MIN_FINAL_SCORE = 0.45


def select_top_segments(scored_segments: List[Dict]) -> List[Dict]:
    """
    Picks the best highlights with enforced temporal diversity.

    Strategy:
      1. Filter out low-quality segments below MIN_FINAL_SCORE.
      2. Iterate score-ranked segments (best first).
      3. Greedily accept a segment only if it is at least MIN_GAP_SECONDS
         away from every already-accepted segment.
      4. Return the final selection sorted chronologically.

    This prevents the common failure mode of selecting 5–6 adjacent
    clips that all cover the same scene or topic.
    """
    if not scored_segments:
        return []

    qualified = [s for s in scored_segments if s.get("final_score", 0) >= MIN_FINAL_SCORE]
    ranked = sorted(qualified, key=lambda s: s["final_score"], reverse=True)

    selected: List[Dict] = []
    for seg in ranked:
        if len(selected) >= MAX_HIGHLIGHTS:
            break
        too_close = any(
            abs(seg["start"] - chosen["start"]) < MIN_GAP_SECONDS
            for chosen in selected
        )
        if not too_close:
            selected.append(seg)

    return sorted(selected, key=lambda s: s["start"])