import re
from llm import call_llm
from tools.file_ops import create_file

def generate_and_write_code(text):
    # figure out filename from user command
    filename = _extract_filename(text) or "generated_code.py"

    prompt = f"""Write clean working Python code for: {text}
Return ONLY the code. No markdown, no explanation."""

    code = call_llm(prompt, system="You are an expert Python developer. Return only raw code.")

    # strip markdown backticks if llm adds them
    code = re.sub(r"^```[\w]*\n?", "", code, flags=re.MULTILINE)
    code = re.sub(r"\n?```$", "", code, flags=re.MULTILINE).strip()

    result = create_file(text, filename=filename, content=code)
    result["output"] = f"saved to output/{filename}\n\n{code[:600]}"
    return result

def _extract_filename(text):
    # try to pull filename from command like "called retry.py" or "named utils.py"
    match = re.search(r"(?:called?|named?|save (?:it )?(?:as|to)?)\s+([\w\-]+\.?\w*)", text, re.IGNORECASE)
    if match:
        name = match.group(1)
        return name if "." in name else name + ".py"
    return None