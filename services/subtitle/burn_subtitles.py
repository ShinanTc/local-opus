import os
import re
import shutil
import subprocess
import tempfile
from typing import List, Dict


# ── Visual constants ────────────────────────────────────────────────────────
FONT_NAME       = "Inter Black"
FONT_SIZE       = 72        # ASS font size — 72 renders clearly on 1080x1920 vertical video
BOTTOM_MARGIN   = 120       # pixels from bottom (MarginV in ASS)
MAX_LINE_CHARS  = 28        # soft-wrap threshold

# Colours — ASS uses &HAABBGGRR (alpha, blue, green, red)
COLOR_DIM       = "&H0090EE90"   # light green — inactive words
COLOR_HIGHLIGHT = "&H00FFFFFF"   # white — active/highlighted word
COLOR_OUTLINE   = "&H99000000"   # dark outline for readability


def _wrap_sentence(sentence: str, max_chars: int = MAX_LINE_CHARS) -> List[str]:
    words, lines, current = sentence.split(), [], ""
    for w in words:
        if not current:
            current = w
        elif len(current) + 1 + len(w) <= max_chars:
            current += " " + w
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def _ass_escape(text: str) -> str:
    """Escape special characters for ASS subtitle text."""
    text = text.replace("\\", "\\\\")
    text = text.replace("{",  "\\{")
    text = text.replace("}",  "\\}")
    return text


def _cs(seconds: float) -> str:
    """Convert seconds to ASS timestamp format: H:MM:SS.cc"""
    h  = int(seconds // 3600)
    m  = int((seconds % 3600) // 60)
    s  = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _build_ass(clip_words: List[Dict]) -> str:
    """
    Build a full ASS subtitle file string with karaoke highlighting.

    Strategy:
    - One ASS dialogue line per sentence.
    - The line uses {\c&color&} to set dim colour, then for each word
      uses {\k<duration>} karaoke tag to advance timing, switching the
      active word to highlight colour with {\c&highlight&} and back with
      {\c&dim&} after.
    - Sentence duration = sentence_start → sentence_end.
    """
    if not clip_words:
        return ""

    # Group words by sentence
    sentence_groups: Dict[tuple, List[Dict]] = {}
    for w in clip_words:
        key = (w["sentence"], w["sentence_start"])
        sentence_groups.setdefault(key, []).append(w)

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{FONT_NAME},{FONT_SIZE},{COLOR_DIM},{COLOR_HIGHLIGHT},{COLOR_OUTLINE},&HCC000000,-1,0,0,0,100,100,0,0,1,2,1,2,20,20,{BOTTOM_MARGIN},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    dialogue_lines = []

    for (sentence, sent_start), words in sentence_groups.items():
        sent_end = words[0]["sentence_end"]

        # Wrap sentence into lines for display
        wrapped_lines = _wrap_sentence(sentence)
        display_text  = "\\N".join(_ass_escape(l) for l in wrapped_lines)

        # Build karaoke tagged text:
        # {\c&dim&}word1{\k50}{\c&hl&}word2{\c&dim&}{\k30}word3...
        # \k duration is in centiseconds
        kar_parts = []
        all_words  = sentence.split()

        # Build a flat word→timing lookup by index
        word_timing = {w["word_index"]: w for w in words}

        # We need to walk through all_words in order, looking up timing
        # for each by index. If a word has no timing entry, we interpolate.
        prev_end = sent_start
        for idx, raw_word in enumerate(all_words):
            wdata     = word_timing.get(idx)
            w_start   = wdata["start"] if wdata else prev_end
            w_end     = wdata["end"]   if wdata else prev_end + 0.2
            dur_cs    = max(1, int(round((w_end - w_start) * 100)))
            prev_end  = w_end

            escaped = _ass_escape(raw_word)
            # Highlight this word during its window, then revert to dim
            kar_parts.append(
                f"{{\\kf{dur_cs}}}{escaped}"
            )

        kar_text = " ".join(kar_parts)

        start_ts = _cs(sent_start)
        end_ts   = _cs(sent_end)

        dialogue_lines.append(
            f"Dialogue: 0,{start_ts},{end_ts},Default,,0,0,0,,{kar_text}"
        )

    return header + "\n".join(dialogue_lines) + "\n"


def burn_subtitles(
    final_paths: List[str],
    clip_words_map: Dict[str, List[Dict]],
    out_dir: str,
) -> List[str]:
    """
    Burns karaoke-style ASS subtitles onto each final clip using FFmpeg's
    `ass=` filter — no fontconfig required, works on Windows.
    """
    os.makedirs(out_dir, exist_ok=True)
    output_paths: List[str] = []

    for clip_path in final_paths:
        clip_name = os.path.basename(clip_path)
        base, ext = os.path.splitext(clip_name)
        out_path  = os.path.join(out_dir, f"{base}_sub{ext}")

        words = clip_words_map.get(clip_path, [])

        if not words:
            print(f"  ⚠️  {clip_name} — no transcript words found, copying as-is")
            shutil.copy2(clip_path, out_path)
            output_paths.append(out_path)
            continue

        print(f"  🔤 {clip_name} — burning {len(words)} word highlights…")

        ass_content = _build_ass(words)
        if not ass_content:
            shutil.copy2(clip_path, out_path)
            output_paths.append(out_path)
            continue

        # Write ASS to a temp file — use forward slashes for FFmpeg on Windows
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ass", delete=False, encoding="utf-8"
        ) as tf:
            tf.write(ass_content)
            ass_path = tf.name

        # FFmpeg on Windows needs forward slashes and escaped colons in paths
        ass_path_ffmpeg = ass_path.replace("\\", "/").replace(":", "\\:")

        try:
            cmd = [
                "ffmpeg", "-y", "-i", clip_path,
                "-vf", f"ass='{ass_path_ffmpeg}'",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-c:a", "copy",
                out_path,
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"  ✗  FFmpeg error for {clip_name}:\n{result.stderr[-2000:]}")
                shutil.copy2(clip_path, out_path)
            else:
                print(f"  ✅ Subtitled: {os.path.basename(out_path)}")

        finally:
            os.unlink(ass_path)

        output_paths.append(out_path)

    return output_paths