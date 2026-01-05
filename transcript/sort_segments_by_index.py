from typing import List, Dict


def sort_segments_by_index(
    segments: List[Dict],
) -> List[Dict]:
    """
    Sorts selected segments by their original transcript index.
    """

    return sorted(
        segments,
        key=lambda seg: seg.get("index", 0)
    )
