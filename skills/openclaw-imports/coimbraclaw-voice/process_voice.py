#!/usr/bin/env python3
"""
coimbraclaw-voice skill - Full voice pipeline
STT → LLM response → TTS
Runs entirely local on VPS.
"""

import sys
import os
import json
import tempfile
import subprocess
from pathlib import Path

# Paths
PIPER_MODEL = "/home/devuser/.openclaw/piper/pt_BR-cadu-medium.onnx"
PIPER_BIN = "/home/devuser/.local/bin/piper"
MEDIA_DIR = "/home/devuser/.openclaw/media/inbound"
OUTPUT_WAV = "/tmp/coimbraclaw_voice_response.wav"

def find_latest_audio():
    """Find the most recent audio file in media/inbound."""
    audio_exts = ['.ogg', '.mp3', '.wav', '.m4a', '.oga', '.opus']
    files = []
    
    if not os.path.exists(MEDIA_DIR):
        print(f"Media dir not found: {MEDIA_DIR}", file=sys.stderr)
        return None
    
    for f in os.listdir(MEDIA_DIR):
        if any(f.lower().endswith(ext) for ext in audio_exts):
            path = os.path.join(MEDIA_DIR, f)
            files.append((os.path.getmtime(path), path))
    
    if not files:
        print("No audio files found in media/inbound", file=sys.stderr)
        return None
    
    # Return most recent
    files.sort(reverse=True)
    return files[0][1]

def transcribe(audio_path):
    """Transcribe audio using Faster-Whisper."""
    print(f"Transcribing: {audio_path}", file=sys.stderr)
    
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel('small', device='cpu', compute_type='int8')
        segments, info = model.transcribe(audio_path, language='pt')
        
        text = ' '.join([seg.text for seg in segments])
        print(f"Transcription: {text}", file=sys.stderr)
        return text
    except Exception as e:
        print(f"STT Error: {e}", file=sys.stderr)
        return None

def synthesize(text):
    """Synthesize text using Piper TTS."""
    print(f"Synthesizing: {text[:50]}...", file=sys.stderr)
    
    try:
        # Write text to temp file for piper
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(text)
            txt_path = f.name
        
        # Generate WAV
        result = subprocess.run(
            [PIPER_BIN, '-m', PIPER_MODEL, '-f', OUTPUT_WAV],
            stdin=subprocess.PIPE,
            input=txt_path.encode(),
            capture_output=True,
            timeout=30
        )
        
        os.unlink(txt_path)
        
        if result.returncode != 0:
            print(f"Piper error: {result.stderr.decode()}", file=sys.stderr)
            return None
        
        return OUTPUT_WAV
    except Exception as e:
        print(f"TTS Error: {e}", file=sys.stderr)
        return None

def main():
    print("=== coimbraclaw-voice ===", file=sys.stderr)
    
    # Step 1: Find audio
    audio_path = find_latest_audio()
    if not audio_path:
        print("NO_AUDIO_FOUND")
        sys.exit(1)
    
    # Step 2: Transcribe
    text = transcribe(audio_path)
    if not text:
        print("TRANSCRIPTION_FAILED")
        sys.exit(1)
    
    # Step 3: Synthesize response
    wav_path = synthesize(text)
    if not wav_path:
        print("SYNTHESIS_FAILED")
        sys.exit(1)
    
    # Output result
    print(f"AUDIO_GENERATED:{wav_path}")
    print(f"TRANSCRIPTION:{text}")

if __name__ == '__main__':
    main()
