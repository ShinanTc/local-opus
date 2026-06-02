import os
from typing import List
from services.video.reformat_clip_to_vertical import reformat_clip_to_vertical


def reformat_all_clips(
    clip_paths: List[str],
    out_dir: str,
) -> List[str]:
    """
    Batch reformats all clips to 9:16 vertical format.

    Returns:
        List[str]: Paths to the reformatted clips.
    """

    os.makedirs(out_dir, exist_ok=True)

    output_paths = []

    for clip_path in clip_paths:
        filename = os.path.basename(clip_path)
        output_path = os.path.join(out_dir, filename)

        print(f"  🎬 Reformatting: {filename}")

        reformat_clip_to_vertical(
            input_path=clip_path,
            output_path=output_path,
        )

        output_paths.append(output_path)

    return output_paths