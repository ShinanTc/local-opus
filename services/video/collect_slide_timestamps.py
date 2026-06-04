import os
from services.video.parse_timestamp_range import parse_timestamp_range


def collect_slide_timestamps(clip_paths: list[str]) -> dict[str, list[tuple[float, float]]]:
    slide_map: dict[str, list[tuple[float, float]]] = {}

    print("\n" + "═" * 60)
    print("  SLIDE TIMESTAMP COLLECTION")
    print("  Review each raw clip and mark slide windows.")
    print("═" * 60)

    for idx, clip_path in enumerate(clip_paths, start=1):
        clip_name = os.path.basename(clip_path)
        print(f"\n[{idx}/{len(clip_paths)}] Clip: {clip_name}")
        print("  Does this clip contain any slide/screen moments?")
        print("  1 → Yes   2 → No")

        while True:
            choice = input("  Your choice (1 or 2): ").strip()
            if choice in ("1", "2"):
                break
            print("  ⚠  Please enter 1 or 2.")

        if choice == "2":
            print("  ↩  Skipping – no slides noted.")
            continue

        ranges = _collect_ranges_for_clip()
        if ranges:
            slide_map[clip_path] = ranges
            print(f"  ✅ {len(ranges)} range(s) saved for {clip_name}")

    print("\n" + "═" * 60)
    print(f"  Slide data collected for {len(slide_map)} clip(s).")
    print("═" * 60 + "\n")
    return slide_map


def _collect_ranges_for_clip() -> list[tuple[float, float]]:
    print()
    print("  Enter one timestamp range per line  (format: MM:SS - MM:SS)")
    print("  When you're done, press Enter on an empty line.")
    print()

    ranges: list[tuple[float, float]] = []
    while True:
        try:
            line = input("  Timestamp: ")
        except EOFError:
            break

        if line.strip() == "":
            if ranges:
                break
            skip = input("  No timestamps yet. Skip this clip? (y/n): ").strip().lower()
            if skip == "y":
                return []
            continue

        try:
            result = parse_timestamp_range(line)
            if result:
                ranges.append(result)
                print(f"  ✔  {line.strip()} → {result[0]:.1f}s – {result[1]:.1f}s")
        except ValueError as e:
            print(f"  ✗  {e}. Try again.")

    return ranges