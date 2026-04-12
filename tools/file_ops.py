import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def _safe_path(filename):
    
    # strip path traversal attempts, always write inside output/

    safe_name = os.path.basename(filename.strip()) or "untitled.txt"
    return os.path.join(OUTPUT_DIR, safe_name)

def create_file(text, filename="output.txt", content=""):
    path = _safe_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return {
        "status": "success",
        "output": f"file created: output/{os.path.basename(path)}",
        "path": path,
    }