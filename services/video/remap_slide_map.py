def remap_slide_map(
    clip_paths: list[str],
    vertical_paths: list[str],
    slide_map: dict[str, list[tuple[float, float]]],
) -> dict[str, list[tuple[float, float]]]:
    """
    slide_map is keyed by original raw clip paths.
    After reformat_all_clips, we need it re-keyed by vertical clip paths
    so apply_slide_fills can look them up correctly.
    """
    remapped: dict[str, list[tuple[float, float]]] = {}
    for orig_path, vert_path in zip(clip_paths, vertical_paths):
        if orig_path in slide_map:
            remapped[vert_path] = slide_map[orig_path]
    return remapped