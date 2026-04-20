import requests

def web_search(text):
    # strip common prefixes
    for prefix in ["search for", "search", "find information about", "find", "look up"]:
        if text.lower().startswith(prefix):
            text = text[len(prefix):].strip()
            break

    if not text:
        return {"status": "error", "output": "nothing to search for."}

    try:
        response = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": text, "format": "json", "no_html": 1, "skip_disambig": 1},
            timeout=10,
        )
        data = response.json()

        results = []

        # check abstract first
        if data.get("AbstractText"):
            results.append(data["AbstractText"])

        # then related topics
        for topic in data.get("RelatedTopics", [])[:3]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append(topic["Text"])

        if not results:
            return {"status": "success", "output": f"no results found for: {text}"}

        output = f"search results for '{text}':\n\n"
        for i, r in enumerate(results[:3], 1):
            output += f"{i}. {r}\n\n"
        return {"status": "success", "output": output}

    except Exception as e:
        return {"status": "error", "output": f"search failed: {e}"}