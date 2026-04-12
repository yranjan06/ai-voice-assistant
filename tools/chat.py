from llm import call_llm

def general_chat(text, context=""):
    prompt = f"{context}\n\nUser: {text}" if context else text
    reply = call_llm(prompt, system="You are a helpful concise assistant.", temperature=0.7)
    return {"status": "success", "output": reply}