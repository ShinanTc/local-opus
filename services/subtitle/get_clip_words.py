import os
import re
from typing import List, Dict


def get_clip_words(
    clip_path: str,
    segments: List[Dict],
) -> List[Dict]:
    """
    Given a final clip path (e.g. `.../20620_79960_final.mp4`) and the full
    transcript segments from parse_transcript(), returns a flat list of words
    whose absolute timestamps fall within the clip's time range, with
    timestamps re-based to clip-local time (i.e. 0.0 = start of clip).

    Each returned word dict also carries the full sentence it belongs to,
    used by the subtitle renderer to draw the dim background sentence.

    Returns:
        [
            {
                "word":          "So",
                "start":         0.0,    # clip-local seconds
                "end":           0.29,
                "sentence":      "So the idea that I want to share...",
                "sentence_start": 0.0,   # clip-local start of the sentence
                "sentence_end":  6.08,   # clip-local end of the sentence
                "word_index":    0,       # index of this word within its sentence
                "word_count":    13,      # total words in its sentence
            },
            ...
        ]
    """
    filename = os.path.basename(clip_path)

    # Strip _final suffix and extension to parse raw clip name
    # Handles both  "20620_79960.mp4"  and  "20620_79960_final.mp4"
    name_stripped = re.sub(r"_final", "", os.path.splitext(filename)[0])

    match = re.match(r"^(\d+)_(\d+)$", name_stripped)
    if not match:
        raise ValueError(
            f"Cannot parse clip timestamps from filename: {filename}\n"
            f"Expected format: {{start_ms}}_{{end_ms}}.mp4 or {{start_ms}}_{{end_ms}}_final.mp4"
        )

    clip_start_s = int(match.group(1)) / 1000.0
    clip_end_s   = int(match.group(2)) / 1000.0

    result: List[Dict] = []

    for seg in segments:
        seg_start = seg["start"]
        seg_end   = seg["end"]

        # Skip segments entirely outside this clip
        if seg_end <= clip_start_s or seg_start >= clip_end_s:
            continue

        words = seg["words"]
        if not words:
            continue

        sentence       = seg["text"]
        sentence_start = max(seg_start - clip_start_s, 0.0)
        sentence_end   = min(seg_end   - clip_start_s, clip_end_s - clip_start_s)
        word_count     = len(words)

        for idx, w in enumerate(words):
            w_start = w["start"]
            w_end   = w["end"]

            # Skip words entirely outside the clip window
            if w_end <= clip_start_s or w_start >= clip_end_s:
                continue

            # Clamp and offset to clip-local time
            local_start = max(w_start - clip_start_s, 0.0)
            local_end   = min(w_end   - clip_start_s, clip_end_s - clip_start_s)

            result.append({
                "word":           w["word"],
                "start":          round(local_start, 3),
                "end":            round(local_end,   3),
                "sentence":       sentence,
                "sentence_start": round(sentence_start, 3),
                "sentence_end":   round(sentence_end,   3),
                "word_index":     idx,
                "word_count":     word_count,
            })

    return result