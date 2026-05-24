import json
from typing import List, Tuple
from config.ai_config import GROQ_CLIENT


def score_segments_batch(
    segments_text: List[str],
    intent_lens: dict,
) -> List[Tuple[float, str]]:
    """
    Single Groq/LLaMA call that scores ALL segments against the intent lens.

    Returns a list of (score_0_to_1, reason) tuples in the same order
    as the input segments_text list.

    Scoring rubric (mapped to 0–1):
      0.9–1.0 : Key insight, strong claim, actionable tip, memorable quote
      0.5–0.8 : Relevant, moderately informative content
      0.0–0.4 : Intro, outro, filler, transitions, greetings, non-speech
    """
    if not segments_text:
        return []

    numbered = "\n".join(f"{i+1}. {t}" for i, t in enumerate(segments_text))
    prompt = (
        f"Niche: {intent_lens['niche']}\n"
        f"Intent: {intent_lens['definition']}\n\n"
        "Score each speech segment 0.0–1.0 for short-form reel highlight quality.\n"
        "1.0 = powerful insight, key revelation, actionable advice, memorable quote.\n"
        "0.0 = intro greeting, outro, filler, transition, or non-speech noise.\n\n"
        f"Segments:\n{numbered}\n\n"
        "Reply ONLY with a JSON array of objects. Each object must have:\n"
        '  "score": float between 0.0 and 1.0\n'
        '  "reason": one short sentence explaining the score\n'
        "Array length must exactly match the number of segments above."
    )

    response = GROQ_CLIENT.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1024,
    )

    raw = response.choices[0].message.content.strip()
    try:
        parsed = json.loads(raw)
        return [(float(item["score"]), item["reason"]) for item in parsed]
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return [(0.5, "Could not parse AI response.")] * len(segments_text)