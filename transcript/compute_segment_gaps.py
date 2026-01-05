from typing import List, Dict


def compute_segment_gaps(
    ordered_segments: List[Dict],
) -> List[Dict]:
    """
    Computes index gaps between adjacent segments.
    Assumes segments are already sorted by index.
    """
    
    if not ordered_segments:
        return []

    result = []
    previous_index = None

    for segment in ordered_segments:
        current_index = segment.get("index", 0)

        if previous_index is None:
            gap = 0
        else:
            gap = current_index - previous_index

        annotated = {
            **segment,
            "gap_from_previous": gap,
            "has_context_gap": gap > 1
        }

        result.append(annotated)
        previous_index = current_index

    return result
