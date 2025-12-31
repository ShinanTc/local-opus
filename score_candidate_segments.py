from typing import List, Dict


def score_candidate_segments(
    candidate_segments: List[Dict],
    niche: str,
) -> List[Dict]:
    """
    Scores each candidate segment based on alignment with the given niche / intent.

    Each segment is expected to have:
        - start
        - end
        - text
    """

    # ---- Step 3A: Build intent lens (single AI call conceptually) ----
    intent_lens = build_intent_lens(niche)

    scored_segments = []

    for segment in candidate_segments:
        # ---- Step 3B: cheap deterministic features ----
        structural_score = compute_structural_score(segment)

        # ---- Step 3C: AI intent-alignment scoring ----
        alignment_score, alignment_reason = score_intent_alignment(
            segment_text=segment["text"],
            intent_lens=intent_lens,
        )

        # ---- Step 3D: final weighted score ----
        final_score = (
            0.4 * alignment_score +
            0.6 * structural_score
        )

        scored_segments.append({
            **segment,
            "alignment_score": alignment_score,
            "structural_score": structural_score,
            "final_score": round(final_score, 3),
            "alignment_reason": alignment_reason,
        })

    # Higher score = better highlight candidate
    scored_segments.sort(key=lambda x: x["final_score"], reverse=True)

    return scored_segments


# ----------------- helpers -----------------


def build_intent_lens(niche: str) -> Dict:
    """
    Conceptual placeholder.
    In reality, this is where a SINGLE AI call would define the intent.
    """
    return {
        "niche": niche,
        "definition": f"Segments valuable for {niche} audience",
    }


def compute_structural_score(segment: Dict) -> float:
    """
    Cheap, deterministic quality score (0–1).
    """
    duration = segment["end"] - segment["start"]

    if duration < 3:
        return 0.2
    if duration > 60:
        return 0.3

    return 0.8


def score_intent_alignment(
    segment_text: str,
    intent_lens: Dict,
) -> tuple[float, str]:
    """
    This is the ONLY place where AI should be used.
    Returns a normalized score (0–1) and a short explanation.
    """

    # Placeholder for GROQ / LLaMA call
    # The model should ONLY judge alignment, nothing else

    score = 0.7  # mock value
    reason = "Expresses a clear idea aligned with the chosen intent."

    return score, reason
