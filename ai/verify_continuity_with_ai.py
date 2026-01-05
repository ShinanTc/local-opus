from typing import List, Dict
from services.ai_continuity import ai_check_continuity


def verify_continuity_with_ai(
    segments: List[Dict],
) -> List[Dict]:
    """
    Phase 3:
    - Only processes segments marked with needs_ai_review = True
    - Merges adjacent risky segments
    - Uses AI to verify continuity
    - Updates segments with AI decision
    """

    if not segments:
        return []

    verified_segments = []
    buffer = []

    def flush_buffer(buf):
        if not buf:
            return []

        merged_text = " ".join(seg["text"] for seg in buf)

        ai_result = ai_check_continuity(merged_text)

        if ai_result["is_continuous"]:
            # Merge into one segment
            return [{
                "start": buf[0]["start"],
                "end": buf[-1]["end"],
                "text": merged_text,
                "lines": sum([seg["lines"] for seg in buf], []),
                "final_score": max(seg["final_score"] for seg in buf),
                "ai_continuous": True,
                "merged_by_ai": True
            }]
        else:
            # Keep them separate, just annotate
            for seg in buf:
                seg["ai_continuous"] = False
                seg["merged_by_ai"] = False
            return buf

    for segment in segments:
        if segment.get("needs_ai_review", False):
            if not buffer:
                buffer.append(segment)
            else:
                prev = buffer[-1]
                if segment["index"] == prev["index"] + 1:
                    buffer.append(segment)
                else:
                    verified_segments.extend(flush_buffer(buffer))
                    buffer = [segment]
        else:
            if buffer:
                verified_segments.extend(flush_buffer(buffer))
                buffer = []
            verified_segments.append(segment)

    if buffer:
        verified_segments.extend(flush_buffer(buffer))

    return verified_segments
