import re
import json
from llm import call_llm

REGEX_PATTERNS = {
    "create_file": re.compile(r"(create|make|new)\s+(a\s+)?(file|folder|directory)", re.IGNORECASE),
    "write_code": re.compile(r"(write|generate|create|build)\s+(a\s+)?(\w+\s+)?(code|script|function|class|program)", re.IGNORECASE),
    "summarize": re.compile(r"(summarize|summary|tldr|shorten|brief|key points)", re.IGNORECASE),
}

KEYWORD_MAP = {
    "create_file": ["file", "folder", "directory", "txt", "json"],
    "write_code": ["code", "python", "function", "class", "script", "algorithm", "program", "implement"],
    "summarize": ["summarize", "summary", "brief", "shorter", "points"],
}

def classify(text):
    # 3 tier intent classifier: regex -> keyword -> llm fallback
    text_lower = text.lower().strip()

    # check for compound commands first
    matched = []
    for intent, pattern in REGEX_PATTERNS.items():
        if pattern.search(text_lower):
            matched.append({"intent": intent, "confidence": "regex", "text": text})

    if len(matched) > 1:
        return matched
    if len(matched) == 1:
        return matched

    # tier 2: keyword scoring
    scores = {k: 0 for k in KEYWORD_MAP}
    for intent, keywords in KEYWORD_MAP.items():
        for kw in keywords:
            if kw in text_lower:
                scores[intent] += 1

    top = max(scores, key=scores.get)
    if scores[top] > 0:
        return [{"intent": top, "confidence": "keyword", "text": text}]

    # tier 3: llm fallback
    return _llm_classify(text)

def _llm_classify(text):
    # ask llm when regex and keywords cant figure it out
    prompt = f"""Classify this user command into one or more intents:
- create_file
- write_code
- summarize
- general_chat

Command: "{text}"

Respond ONLY with valid JSON array. Example: [{{"intent": "write_code", "confidence": "llm"}}]
For compound commands return multiple: [{{"intent": "summarize", "confidence": "llm"}}, {{"intent": "create_file", "confidence": "llm"}}]"""

    try:
        response = call_llm(prompt, system="You are an intent classifier. Only respond with valid JSON.")
        json_match = re.search(r'\[.*?\]', response, re.DOTALL)
        if json_match:
            intents = json.loads(json_match.group())
            for item in intents:
                item["text"] = text
            return intents
    except Exception:
        pass

    return [{"intent": "general_chat", "confidence": "fallback", "text": text}]