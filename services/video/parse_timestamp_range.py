import re


def parse_timestamp_range(line: str) -> tuple[float, float] | None:
    line = line.strip()
    if not line:
        return None

    parts = re.split(r"\s*-\s*", line)
    if len(parts) != 2:
        raise ValueError(f"Expected format 'MM:SS - MM:SS' but got: '{line}'")

    start = _parse_timestamp(parts[0])
    end   = _parse_timestamp(parts[1])

    if end <= start:
        raise ValueError(
            f"End time ({parts[1]}) must be after start time ({parts[0]})"
        )
    return (start, end)


def _parse_timestamp(ts: str) -> float:
    ts = ts.strip()
    match = re.fullmatch(r"(\d{1,2}):(\d{2})", ts)
    if not match:
        raise ValueError(
            f"Invalid timestamp format '{ts}'. Use MM:SS (e.g. 01:30)"
        )
    minutes = int(match.group(1))
    seconds = int(match.group(2))
    if seconds >= 60:
        raise ValueError(f"Seconds value '{seconds}' must be < 60")
    return float(minutes * 60 + seconds)