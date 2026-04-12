from llm import call_llm

def summarize_text(text):
    # strip common prefixes like "summarize this:"
    for prefix in ["summarize this:", "summarize:", "summarize this text:", "tldr:"]:
        if text.lower().startswith(prefix):
            text = text[len(prefix):].strip()
            break

    if len(text.split()) < 10:
        return {"status": "warning", "output": "text too short to summarize."}

    summary = call_llm(
        f"Summarize in 3-5 bullet points starting with -:\n{text}",
        system="You are a concise summarizer."
    )
    return {"status": "success", "output": summary}