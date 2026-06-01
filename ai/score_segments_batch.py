import json
from typing import List, Tuple
from config.ai_config import GROQ_CLIENT

SCORING_MODEL = "llama-3.1-8b-instant"


def score_segments_batch(
    segments_text: List[str],
    intent_lens: dict,
) -> List[Tuple[float, str]]:
    """
    Single Groq call scoring all segments against the intent lens.
    Uses llama-3.1-8b-instant — current fastest small model on Groq,
    250K TPM limit, significantly higher than 70b.
    Returns (score_0_to_1, reason) tuples in input order.
    """
    if not segments_text:
        return []

    numbered = "\n".join(f"{i+1}. {t}" for i, t in enumerate(segments_text))
    prompt = (
        f"Niche: {intent_lens['niche']}\n"
        f"Intent: {intent_lens['definition']}\n\n"
        "Score each segment 0.0-1.0 for short-form reel quality.\n"
        "1.0=key insight, actionable advice, memorable quote.\n"
        "0.0=intro, outro, filler, greeting, transition.\n\n"
        f"{numbered}\n\n"
        'Reply ONLY with a JSON array: [{"score":0.0,"reason":"..."},...] '
        "Same length as input. No markdown."
    )

    response = GROQ_CLIENT.chat.completions.create(
        model=SCORING_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=512,
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        parsed = json.loads(raw)
        return [(float(item["score"]), item["reason"]) for item in parsed]
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return [(0.5, "Could not parse AI response.")] * len(segments_text)