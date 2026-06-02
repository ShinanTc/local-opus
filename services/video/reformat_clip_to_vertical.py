import subprocess


def reformat_clip_to_vertical(
    input_path: str,
    output_path: str,
):
    """
    Convert a clip to 9:16 vertical format using a center crop.
    """

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-vf",
        "crop=ih*9/16:ih,scale=1080:1920",
        "-c:a",
        "copy",
        output_path,
    ]

    subprocess.run(cmd, check=True)