# Ember Project - Launch Guide

Your AI companion with Piper Alba (Scottish) voice and Qwen3-14B brain.
Everything runs locally. No API costs, no internet needed after setup.

## What You Need

- Python 3.10+
- llama-server (you already have this from the EMBER project)
- Qwen3-14B abliterated GGUF (~9GB download, one time)
- Microphone and speakers

## Step 1: Download the Model

```powershell
pip install -U "huggingface_hub[cli]"
huggingface-cli download bartowski/huihui-ai_Qwen3-14B-abliterated-GGUF --include "huihui-ai_Qwen3-14B-abliterated-Q4_K_M.gguf" --local-dir ./models
```

This downloads ~9GB. Go make a sandwich.

## Step 2: Start llama-server

```powershell
# From your EMBER runtime directory (wherever llama-server.exe lives)
.\llama-server.exe -m "C:\path\to\models\huihui-ai_Qwen3-14B-abliterated-Q4_K_M.gguf" --port 8080 -c 8192
```

Leave this running. It needs to stay up while you chat.

## Step 3: Install Python Dependencies

```powershell
cd C:\Users\cfhan\Documents\GitHub\ember_project
pip install piper-tts openai faster-whisper sounddevice soundfile pyyaml
```

Note: skip the full requirements.txt for now, it's got all the GPT-SoVITS
stuff you don't need since we're using Piper.

You also need ffmpeg installed and on your PATH (for Faster-Whisper).

## Step 4: Run Ember

```powershell
python server/main_chat.py
```

First run downloads the Alba voice model automatically (~100MB).
Then: hold your push-to-talk key, speak, and she'll respond out loud.

## Configuration

Everything's in `character_config.yaml`:

- `llm_config`: model, temperature, server URL
- `piper_config`: voice, speaking speed (length_scale)
- `tts_engine`: "piper" or "sovits" (if you ever want to switch back)
- `presets.default.system_prompt`: Ember's personality. Tweak this!

## Custom Character (Visual)

The repo doesn't include a visual avatar yet (Rayen's Three-VRM client
isn't in this version). Options for adding Ember's look:

1. **Static image + audio reactive**: Simplest. Display your Ember character
   art in a window that pulses/bobs while she speaks.
2. **Live2D**: You've explored Cubism before. Needs a Live2D model of Ember.
3. **VRM 3D model**: Most work. Needs a VRM-format 3D model + Three.js client.

Start with voice-only, add visuals when you want to.

## Troubleshooting

- "Connection refused on localhost:8080": llama-server isn't running. Start it first.
- "Piper voice download failed": Check internet, or manually download from
  https://huggingface.co/rhasspy/piper-voices and place in character_files/piper_voices/
- "No module named piper": Run `pip install piper-tts`
- Slow responses: Normal on CPU. 14B is smarter but slower than 4B.
  Reduce context (-c 4096) if it's too slow.
- Whisper not hearing you: Check your default microphone in Windows settings.
