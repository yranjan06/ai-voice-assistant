import os
import requests

def transcribe(audio_path):
    api_key = os.environ.get("GROQ_API_KEY")                           #send audio to groq whisper api and get text back
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY not set in environment")

    model = os.environ.get("STT_MODEL", "whisper-large-v3")

    with open(audio_path, "rb") as f:
        response = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (os.path.basename(audio_path), f, "audio/wav")},
            data={"model": model, "response_format": "json"},
            timeout=30,
        )

    if response.status_code != 200:
        raise RuntimeError(f"STT failed ({response.status_code}): {response.text}")

    return response.json().get("text", "").strip()