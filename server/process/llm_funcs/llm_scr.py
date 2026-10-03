"""LLM chat with history - works with any OpenAI-compatible API.

Supports:
- Local llama-server (Qwen 4B) via base_url
- OpenAI API (set base_url to default, provide api_key)
- Any other OpenAI-compatible endpoint

Configure in character_config.yaml under llm_config.
"""
import yaml
import json
import os
from openai import OpenAI

with open('character_config.yaml', 'r') as f:
    char_config = yaml.safe_load(f)

_llm = char_config.get('llm_config', {})
BASE_URL = _llm.get('base_url', None)  # None = OpenAI default
API_KEY = _llm.get('api_key', 'not-needed')  # local servers don't check this
MODEL = _llm.get('model', char_config.get('model', 'gpt-4.1-mini'))
TEMPERATURE = _llm.get('temperature', 0.8)

if BASE_URL:
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
else:
    client = OpenAI(api_key=API_KEY)

HISTORY_FILE = char_config.get('history_file', 'chat_history.json')
SYSTEM_PROMPT = char_config['presets']['default']['system_prompt']


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return [{"role": "system", "content": SYSTEM_PROMPT}]


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def llm_response(user_input):
    messages = load_history()

    # Append user message
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=2048,
    )

    reply = response.choices[0].message.content or ""

    # Append assistant reply
    messages.append({"role": "assistant", "content": reply})
    save_history(messages)
    return reply


if __name__ == "__main__":
    print("Testing LLM connection...")
    print(llm_response("Say hello!"))
