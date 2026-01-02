from typing import List, Dict

def identify_gap_risks(
    segments: List[Dict],
    gap_threshold: int = 1
) -> List[Dict]:
    """
    Flags segments whose gap from the previous segment exceeds the threshold.
    
    Adds:
      - "gap_risk": True/False
      - "gap_risk_level": "low"/"high" (optional, for logging or future scoring)
    """

    if not segments:
        return []

    flagged_segments = []
    
    for segment in segments:
        gap = segment.get("gap_from_previous", 0)

        if gap > gap_threshold:
            segment["gap_risk"] = True
            segment["gap_risk_level"] = "high"
        else:
            segment["gap_risk"] = False
            segment["gap_risk_level"] = "low"

        flagged_segments.append(segment)

    return flagged_segments
