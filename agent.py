from dotenv import load_dotenv
load_dotenv()

from stt import transcribe
from intent import classify
from tools import TOOL_MAP
from tools.chat import general_chat
from utils.audio import convert_to_wav
from memory import SessionMemory

_memory = SessionMemory()

def run(audio_path):
    result = {"transcription": "", "intent": "", "confidence": "", "action": "", "output": ""}

    # step 1: convert audio
    try:
        wav_path = convert_to_wav(audio_path)
    except Exception as e:
        result["output"] = f"audio conversion failed: {e}"
        return result

    # step 2: transcribe
    try:
        text = transcribe(wav_path)
        result["transcription"] = text
        if not text:
            result["output"] = "could not transcribe audio."
            return result
    except Exception as e:
        result["output"] = f"stt failed: {e}"
        return result

    # step 3: classify intent
    try:
        intents = classify(text)
    except Exception:
        intents = [{"intent": "general_chat", "confidence": "fallback", "text": text}]

    result["intent"] = intents[0]["intent"]
    result["confidence"] = intents[0].get("confidence", "unknown")

    # step 4: execute tool
    try:
        tool_fn = TOOL_MAP.get(result["intent"], general_chat)
        # inject memory context for chat
        if result["intent"] == "general_chat":
            context = _memory.get_context()
            tool_result = general_chat(text, context=context)
        else:
            tool_result = tool_fn(text)
        result["action"] = f"executed: {result['intent']}"
        result["output"] = tool_result.get("output", "done")
    except Exception as e:
        result["action"] = "failed"
        result["output"] = f"tool error: {e}"

    # step 5: save to memory
    _memory.add(text, result["intent"], {"output": result["output"]})

    return result

def get_history():
    return _memory.get_all()