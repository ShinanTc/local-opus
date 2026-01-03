from typing import Dict
import json

from config.ai_config import GROQ_CLIENT


def ai_check_continuity(text: str) -> Dict:
    """
    Phase 3 AI helper.

    Determines whether the given merged text represents
    a single continuous context or a context jump.

    Returns:
    {
        "is_continuous": bool,
        "reason": str
    }
    """

    prompt = f"""
You are analyzing transcript excerpts from a long-form video.

Task:
Decide whether the following text represents ONE continuous topic
or if the speaker jumps to a DIFFERENT topic.

Rules:
- Minor tangents, examples, or elaborations count as CONTINUOUS
- Clear subject changes count as DISCONTINUOUS
- Ignore stylistic changes

Text:
{text}

Respond ONLY in valid JSON with no extra text:

{{
  "is_continuous": true or false,
  "reason": "brief explanation"
}}
"""

    try:
        response_text = GROQ_CLIENT(prompt)

        # If your call_llama already returns dict, handle safely
        if isinstance(response_text, dict):
            return {
                "is_continuous": bool(response_text.get("is_continuous", False)),
                "reason": response_text.get("reason", "")
            }

        parsed = json.loads(response_text)

        return {
            "is_continuous": bool(parsed.get("is_continuous", False)),
            "reason": parsed.get("reason", "")
        }

    except Exception as e:
        # Fail-safe: if AI fails, assume discontinuity (safer choice)
        return {
            "is_continuous": False,
            "reason": f"AI continuity check failed: {str(e)}"
        }
