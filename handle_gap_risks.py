from typing import List, Dict

def handle_gap_risks(
    segments: List[Dict],
    penalty_for_gap_risk: float = 0.1,
    drop_low_score_threshold: float = 0.5
) -> List[Dict]:
    """
    Phase 2: Rule-based handling of segments with flagged gaps.
    
    Logic:
      - If a segment has gap_risk=True, decrease its final_score by `penalty_for_gap_risk`.
      - If the adjusted final_score falls below `drop_low_score_threshold`, mark segment as dropped.
      - Otherwise, keep segment as is.
    
    Adds:
      - "adjusted_final_score"
      - "dropped_due_to_gap_risk" (True/False)
    """

    updated_segments = []

    for segment in segments:
        adjusted_score = segment.get("final_score", 0.0)

        if segment.get("gap_risk", False):
            adjusted_score -= penalty_for_gap_risk
            # Ensure score doesn't go negative
            adjusted_score = max(0.0, adjusted_score)

        segment["adjusted_final_score"] = adjusted_score
        segment["dropped_due_to_gap_risk"] = adjusted_score < drop_low_score_threshold

        updated_segments.append(segment)

    return updated_segments
