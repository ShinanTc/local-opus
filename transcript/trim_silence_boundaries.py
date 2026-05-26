from typing import List, Dict

SILENCE_THRESHOLD = 6.0


def trim_silence_boundaries(lines: List[Dict]) -> List[Dict]:
    """
    Trims intro and outro lines by detecting 6+ second silence gaps
    at the start and end of the transcript.
    """
    if not lines:
        return []
    lines = _trim_intro(lines)
    lines = _trim_outro(lines)
    return lines


def _trim_intro(lines: List[Dict]) -> List[Dict]:
    """
    Drops everything up to and including the last 6s+ silence gap
    in the first 120 seconds of the video.
    """
    cut_index = 0

    for i in range(len(lines) - 1):
        if lines[i]["end"] > 120.0:
            break
        gap = lines[i + 1]["start"] - lines[i]["end"]
        if gap >= SILENCE_THRESHOLD:
            cut_index = i + 1

    return lines[cut_index:]


def _trim_outro(lines: List[Dict]) -> List[Dict]:
    """
    Drops everything from the first 6s+ silence gap
    in the last 120 seconds of the video.
    """
    video_end = lines[-1]["end"]
    cut_index = len(lines)

    for i in range(len(lines) - 1):
        if lines[i]["start"] < video_end - 120.0:
            continue
        gap = lines[i + 1]["start"] - lines[i]["end"]
        if gap >= SILENCE_THRESHOLD:
            cut_index = i + 1
            break

    return lines[:cut_index]