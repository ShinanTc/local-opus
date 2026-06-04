import os
import shutil
import subprocess
from services.video.build_slide_filtergraph import build_slide_filtergraph


def apply_slide_fills(
    clip_paths: list[str],
    slide_map: dict[str, list[tuple[float, float]]],
    out_dir: str,
) -> list[str]:
    os.makedirs(out_dir, exist_ok=True)
    output_paths: list[str] = []

    for clip_path in clip_paths:
        clip_name = os.path.basename(clip_path)
        base, ext = os.path.splitext(clip_name)
        out_path  = os.path.join(out_dir, f"{base}_final{ext}")

        if clip_path not in slide_map:
            print(f"  ✂  {clip_name} – plain 9:16 crop…")
            success = _run_plain_vertical_crop(clip_path, out_path)
        else:
            print(f"  🎬 {clip_name} – applying slide fills…")
            filtergraph, last_label = build_slide_filtergraph(slide_map[clip_path])
            success = _run_ffmpeg(clip_path, filtergraph, last_label, out_path)

        if not success:
            shutil.copy2(clip_path, out_path)

        output_paths.append(out_path)

    return output_paths


def _run_plain_vertical_crop(clip_path: str, out_path: str) -> bool:
    cmd = [
        "ffmpeg", "-y", "-i", clip_path,
        "-vf", "crop=ih*9/16:ih,scale=1080:1920",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        out_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ✗  FFmpeg crop error:\n{result.stderr[-2000:]}")
        return False
    return True


def _run_ffmpeg(
    clip_path: str, filtergraph: str, last_label: str, out_path: str
) -> bool:
    cmd = [
        "ffmpeg", "-y", "-i", clip_path,
        "-filter_complex", filtergraph,
        "-map", last_label,
        "-map", "0:a?",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        out_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ✗  FFmpeg error:\n{result.stderr[-2000:]}")
        return False
    print(f"  ✅ Saved: {os.path.basename(out_path)}")
    return True