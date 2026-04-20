#!/usr/bin/env python3
"""Transcribe a single inbound audio file for OpenClaw media.audio CLI mode."""

import os
import re
import sys
from pathlib import Path

from faster_whisper import WhisperModel

MODEL_NAME = os.environ.get("COIMBRACLAW_WHISPER_MODEL", "small")
LANGUAGE = os.environ.get("COIMBRACLAW_WHISPER_LANGUAGE", "pt")
DEVICE = os.environ.get("COIMBRACLAW_WHISPER_DEVICE", "cpu")
COMPUTE_TYPE = os.environ.get("COIMBRACLAW_WHISPER_COMPUTE", "int8")
MIN_BYTES = 1024


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: transcribe_audio.py <media-path>", file=sys.stderr)
        return 2

    media_path = Path(sys.argv[1]).expanduser()
    if not media_path.is_file():
        print(f"audio file not found: {media_path}", file=sys.stderr)
        return 1

    if media_path.stat().st_size < MIN_BYTES:
        print(f"audio file too small: {media_path}", file=sys.stderr)
        return 1

    model = WhisperModel(MODEL_NAME, device=DEVICE, compute_type=COMPUTE_TYPE)
    segments, _ = model.transcribe(
        str(media_path),
        language=LANGUAGE,
        vad_filter=True,
        beam_size=5,
        condition_on_previous_text=False,
    )

    transcript = normalize_text(
        " ".join(segment.text.strip() for segment in segments if segment.text.strip())
    )
    if not transcript:
        print(f"empty transcript for: {media_path}", file=sys.stderr)
        return 1

    sys.stdout.write(transcript)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
