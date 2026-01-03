MAX_HIGHLIGHT_DURATION = 60  # seconds, adjustable

def merge_continuous_segments(segments: list) -> list:
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
