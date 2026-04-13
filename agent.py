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

    # step 3: classify intent (can return multiple for compound commands)
    try:
        intents = classify(text)
    except Exception:
        intents = [{"intent": "general_chat", "confidence": "fallback", "text": text}]

    result["intent"] = " + ".join(i["intent"] for i in intents)
    result["confidence"] = intents[0].get("confidence", "unknown")

    # step 4: execute tools sequentially
    outputs = []
    actions = []
    try:
        for intent_obj in intents:
            name = intent_obj["intent"]
            tool_fn = TOOL_MAP.get(name, general_chat)
            if name == "general_chat":
                context = _memory.get_context()
                tool_result = general_chat(text, context=context)
            else:
                tool_result = tool_fn(text)
            outputs.append(tool_result.get("output", "done"))
            actions.append(name)
    except Exception as e:
        outputs.append(f"tool error: {e}")

    result["action"] = "executed: " + " + ".join(actions)
    result["output"] = "\n\n---\n\n".join(outputs)

    # step 5: save to memory
    _memory.add(text, result["intent"], {"output": result["output"]})

    return result

def get_history():
    return _memory.get_all()