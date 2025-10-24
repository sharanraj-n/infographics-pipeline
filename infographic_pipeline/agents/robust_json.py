import json
import re

def robust_json_extract(text):
    """
    Extracts a JSON object from a string, being tolerant to LLMs returning extra text.
    """
    matches = re.findall(r'\{[\s\S]*\}', text)
    for candidate in matches:
        try:
            return json.loads(candidate)
        except Exception:
            continue
    try:
        return json.loads(text)
    except Exception:
        return {"error": "Failed to extract JSON", "raw": text}
