TARGET_W = 1080
TARGET_H = 1920


def build_slide_filtergraph(ranges: list[tuple[float, float]]) -> tuple[str, str]:
    """
    Builds an ffmpeg filter_complex string where:
      - Base stream: standard 9:16 centre-crop (whole video)
      - Inside timestamp windows only: blurred+zoomed background with the
        landscape frame centred on top, overlaid over the base stream
    Returns (filtergraph_string, final_output_label).
    """
    filter_parts: list[str] = []

    # Base: normal 9:16 centre-crop — this is what plays for the entire video
    filter_parts.append(
        f"[0:v]crop=ih*9/16:ih,scale={TARGET_W}:{TARGET_H}[base]"
    )

    last_label = "[base]"

    for i, (t_start, t_end) in enumerate(ranges):
        bg_label   = f"[bg{i}]"
        fg_label   = f"[fg{i}]"
        comp_label = f"[comp{i}]"
        out_label  = f"[v{i}]"

        # Background: original landscape frame zoomed+blurred to fill 1080x1920
        filter_parts.append(
            f"[0:v]scale={TARGET_W}:{TARGET_H}:force_original_aspect_ratio=increase,"
            f"crop={TARGET_W}:{TARGET_H},"
            f"gblur=sigma=30{bg_label}"
        )

        # Foreground: original landscape frame scaled to 1080px wide, AR preserved
        filter_parts.append(
            f"[0:v]scale={TARGET_W}:-2{fg_label}"
        )

        # Composite: blurred bg + landscape fg centred on top
        filter_parts.append(
            f"{bg_label}{fg_label}overlay="
            f"(W-w)/2:(H-h)/2"
            f"{comp_label}"
        )

        # Splice: overlay the composite onto the base stream, ONLY during the window
        filter_parts.append(
            f"{last_label}{comp_label}overlay="
            f"0:0:enable='between(t,{t_start},{t_end})'"
            f"{out_label}"
        )

        last_label = out_label

    return "; ".join(filter_parts), last_label