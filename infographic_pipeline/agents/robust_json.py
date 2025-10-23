"""
Utility module for robust extraction of JSON from LLM responses.
Handles cases where model output is not STRICTLY a JSON block.
"""

import json, re

def robust_json_extract(text):
    """
    Attempt to extract the first valid JSON object from a model string output.
    - Tries parsing all {...} blocks (most common LLM "leakage" format).
    - Falls back to trying the entire output.
    - Returns dict, or {error, raw} if unsuccessful.
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
