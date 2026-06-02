from typing import List, Dict
from services.video.extract_frame import extract_frame_as_base64
from ai.analyze_frame_crop_mode import analyze_frame_crop_mode

SAMPLE_INTERVAL_SECONDS = 2.0
PRESERVE_CONFIDENCE_THRESHOLD = 0.75


def detect_crop_modes_for_clip(
    clip_path: str,
    start: float,
    end: float,
) -> List[Dict]:
    """
    Samples frames across the clip at regular intervals and returns
    a crop mode decision for each sampled timestamp.

    A frame triggers preserve-full-frame only if:
      - AI returns preserve_full_frame = True
      - confidence >= PRESERVE_CONFIDENCE_THRESHOLD
    """
    decisions = []
    timestamp = start

    while timestamp < end:
        frame_b64 = extract_frame_as_base64(clip_path, timestamp)
        decision = analyze_frame_crop_mode(frame_b64)

        confirmed_preserve = (
            decision.get("preserve_full_frame", False)
            and decision.get("confidence", 0.0) >= PRESERVE_CONFIDENCE_THRESHOLD
        )

        decisions.append({
            "timestamp": round(timestamp, 2),
            "preserve_full_frame": confirmed_preserve,
            "confidence": decision.get("confidence", 0.0),
            "reason": decision.get("reason", ""),
        })
        timestamp += SAMPLE_INTERVAL_SECONDS

    return decisions