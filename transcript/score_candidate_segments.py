from typing import List, Dict
from ai.score_segments_batch import score_segments_batch


def score_candidate_segments(
    candidate_segments: List[Dict],
    niche: str,
) -> List[Dict]:
    """
    Scores each candidate segment using structural features + AI alignment.
    Returns segments sorted by final_score descending.
    """
    if not candidate_segments:
        return []

    intent_lens = _build_intent_lens(niche)
    texts = [seg["text"] for seg in candidate_segments]
    ai_results = score_segments_batch(texts, intent_lens)

    scored = []
    for seg, (alignment_score, alignment_reason) in zip(candidate_segments, ai_results):
        structural_score = _compute_structural_score(seg)
        final_score = round(0.4 * alignment_score + 0.6 * structural_score, 3)
        scored.append({
            **seg,
            "alignment_score": alignment_score,
            "structural_score": structural_score,
            "final_score": final_score,
            "alignment_reason": alignment_reason,
        })

    scored.sort(key=lambda x: x["final_score"], reverse=True)
    return scored


def _build_intent_lens(niche: str) -> Dict:
    """
    Builds the intent context passed to AI for alignment scoring.
    Single source of truth for what makes a good highlight in this niche.
    """
    return {
        "niche": niche,
        "definition": f"Segments that are genuinely valuable and insightful for a {niche} audience",
    }


def _compute_structural_score(segment: Dict) -> float:
    """
    Cheap deterministic quality signal based on segment duration (0–1).
    Penalises clips that are too short or excessively long.
    """
    duration = segment["end"] - segment["start"]
    if duration < 3:
        return 0.2
    if duration > 60:
        return 0.3
    return 0.8