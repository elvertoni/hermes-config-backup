---
name: coimbraclaw-voice
description: Process voice messages — STT (Whisper) → respond → TTS (Piper pt-BR). Use when user sends audio/voice message.
metadata:
  supports:
    - audio_input
    - audio_output
  requires:
    bins: []
    python_packages:
      - faster-whisper
      - piper-tts
---

# coimbraclaw-voice

Processes voice messages using local STT and TTS.

## How it works

1. OpenClaw downloads inbound voice/audio into `media/inbound/`
2. `tools.media.audio` calls `transcribe_audio.py` with the exact `{{MediaPath}}`
3. Faster-Whisper transcribes the file in pt-BR
4. OpenClaw injects the transcript into `{{Transcript}}` before agent processing
5. Optional TTS can still be produced with Piper for outbound audio replies

## Usage

Inbound transcription is handled natively by OpenClaw media understanding. This skill keeps the local STT/TTS assets and helper scripts together.

## Audio Processing

- STT: Faster-Whisper small (int8 CPU) via `transcribe_audio.py`
- TTS: Piper pt-BR cadu-medium (60MB, 100% local)
- Both run on the VPS — no external API calls

## Output

- `transcribe_audio.py` prints plain transcript text to stdout for OpenClaw
- `process_voice.py` remains available for explicit STT → TTS workflows
