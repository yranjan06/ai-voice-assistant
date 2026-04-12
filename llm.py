import os
import json
import requests

def call_llm(prompt, system="You are a helpful assistant.", temperature=0.3):
    
    api_key = os.environ.get("GROQ_API_KEY")                          # shared groq llama wrapper used by intent classifier and tools
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY not set")

    model = os.environ.get("LLM_MODEL", "llama3-70b-8192")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": 2048,
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError(f"LLM error ({response.status_code}): {response.text}")

    return response.json()["choices"][0]["message"]["content"].strip()