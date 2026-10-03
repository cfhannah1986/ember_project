"""Piper TTS for Ember - drop-in replacement for GPT-SoVITS.

Uses Piper's Alba voice (Scottish accent) for local neural TTS.
No server needed, runs entirely on-device.

Install: pip install piper-tts
Voice model auto-downloads on first run.
"""
import subprocess
import sys
from pathlib import Path

import soundfile as sf
import sounddevice as sd
import yaml

# Load config
_config_path = Path(__file__).resolve().parent.parent.parent / "character_config.yaml"
with open(_config_path, 'r') as f:
    _config = yaml.safe_load(f)

_piper_config = _config.get('piper_config', {})
VOICE = _piper_config.get('voice', 'en_GB-alba-medium')
MODEL_DIR = Path(_piper_config.get('model_dir', 'character_files/piper_voices'))
SPEAKER = _piper_config.get('speaker', 0)
LENGTH_SCALE = _piper_config.get('length_scale', 1.0)


def _ensure_voice():
    """Download the Alba voice model if not present."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    onnx = MODEL_DIR / f"{VOICE}.onnx"
    json_cfg = MODEL_DIR / f"{VOICE}.onnx.json"
    if onnx.exists() and json_cfg.exists():
        return onnx
    print(f"Downloading Piper voice '{VOICE}'...")
    url_base = f"https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alba/medium/{VOICE}"
    import urllib.request
    for suffix in [".onnx", ".onnx.json"]:
        url = url_base + suffix
        dest = MODEL_DIR / (VOICE + suffix)
        if not dest.exists():
            print(f"  {url}")
            urllib.request.urlretrieve(url, dest)
    return onnx


def play_audio(path):
    data, samplerate = sf.read(path)
    sd.play(data, samplerate)
    sd.wait()


def piper_gen(in_text, output_wav_pth="output.wav"):
    """Generate speech with Piper. Same interface as sovits_gen."""
    try:
        model_path = _ensure_voice()
    except Exception as e:
        print(f"Error downloading voice model: {e}")
        return None

    try:
        cmd = [
            sys.executable, "-m", "piper",
            "--model", str(model_path),
            "--output_file", output_wav_pth,
        ]
        if SPEAKER:
            cmd += ["--speaker", str(SPEAKER)]
        if LENGTH_SCALE != 1.0:
            cmd += ["--length_scale", str(LENGTH_SCALE)]

        proc = subprocess.run(
            cmd, input=in_text.encode("utf-8"),
            capture_output=True, timeout=60,
        )
        if proc.returncode != 0:
            print(f"Piper error: {proc.stderr.decode()[:200]}")
            return None
        return output_wav_pth
    except Exception as e:
        print(f"Error in piper_gen: {e}")
        return None


# Alias for drop-in compatibility
tts_gen = piper_gen


if __name__ == "__main__":
    out = piper_gen("Hello! I'm Ember. Nice to meet you!")
    if out:
        print(f"Saved to {out}")
        play_audio(out)
