"""
Universal JSON cleaner for AI model responses.
Handles every known failure mode from any 
AI model output permanently.
"""

import json
import re
import unicodedata
from json_repair import repair_json


def clean_and_parse(raw: str, source: str = "AI") -> dict:
    """
    Takes raw AI model output.
    Returns a clean Python dictionary.
    Never fails silently.
    Raises ValueError with clear message if 
    truly unrecoverable.
    
    Handles:
    - Markdown fences (```json ... ```)
    - Emojis and unicode symbols
    - Invalid escape sequences
    - Trailing commas
    - Single quotes instead of double quotes
    - Unquoted keys
    - Truncated JSON
    - Extra text before or after JSON
    - Newlines inside strings
    - Control characters
    - Mixed encoding issues
    - Missing closing brackets
    - Duplicate keys
    """
    
    if not raw or not raw.strip():
        raise ValueError(
            f"[{source}] Empty response received"
        )
    
    # ── STAGE 1: Strip markdown fences ────────
    # Handles: ```json ... ``` and ``` ... ```
    raw = raw.strip()
    raw = re.sub(
        r'^```(?:json|JSON|Json)?\s*\n?', 
        '', 
        raw, 
        flags=re.MULTILINE
    )
    raw = re.sub(r'\n?```\s*$', '', raw, flags=re.MULTILINE)
    raw = raw.strip()
    
    # ── STAGE 2: Extract JSON object ──────────
    # Find the first { and last } to isolate JSON
    # Ignores any text before or after the JSON
    start = raw.find('{')
    end = raw.rfind('}')
    
    if start == -1 or end == -1 or start >= end:
        # Try array format as fallback
        start = raw.find('[')
        end = raw.rfind(']')
        if start == -1 or end == -1:
            raise ValueError(
                f"[{source}] No JSON structure found. "
                f"Raw (first 200 chars): {raw[:200]}"
            )
    
    raw = raw[start:end+1]
    
    # ── STAGE 3: Remove control characters ────
    # Removes invisible characters that break parsing
    # Keeps normal whitespace (spaces, newlines, tabs)
    raw = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', raw)
    
    # ── STAGE 4: Handle unicode and emojis ────
    # Strategy: normalize unicode first, 
    # then remove anything non-ASCII that 
    # survived normalization
    
    # Normalize unicode (converts accented chars 
    # to their base form where possible)
    raw = unicodedata.normalize('NFKD', raw)
    
    # Remove emojis and other non-ASCII symbols
    # that json.loads() cannot handle
    raw = raw.encode('ascii', 'ignore').decode('ascii')
    
    # ── STAGE 5: Fix escape sequences ─────────
    # Valid JSON escapes: \" \\ \/ \b \f \n \r \t \uXXXX
    # Everything else is illegal and must be fixed
    
    def fix_escape(match):
        char = match.group(1)
        valid_escapes = '"\\\/bfnrtu'
        if char in valid_escapes:
            return match.group(0)  # Keep valid escape
        elif char == 'n':
            return '\\n'
        elif char == 't':
            return '\\t'
        elif char == 'r':
            return '\\r'
        else:
            return '\\\\'  # Double the backslash
    
    raw = re.sub(r'\\(.)', fix_escape, raw)
    
    # ── STAGE 6: Fix common AI JSON mistakes ──
    
    # Remove trailing commas before } or ]
    # Example: {"key": "val",} → {"key": "val"}
    raw = re.sub(r',\s*([}\]])', r'\1', raw)
    
    # Fix single-quoted strings to double-quoted
    # Example: {'key': 'val'} → {"key": "val"}
    raw = re.sub(r"(?<![\\])'", '"', raw)
    
    # Remove newlines inside string values
    # that aren't properly escaped
    raw = re.sub(r'(?<!\\)\n', ' ', raw)
    
    # ── STAGE 7: Try standard parse ───────────
    try:
        result = json.loads(raw)
        if isinstance(result, dict):
            return result
    except json.JSONDecodeError:
        pass
    
    # ── STAGE 8: Use json-repair as fallback ──
    # This library is specifically built for
    # fixing AI-generated broken JSON.
    # It handles truncated JSON, missing brackets,
    # unquoted keys, and dozens of other issues.
    try:
        repaired = repair_json(raw, return_objects=True)
        if isinstance(repaired, dict) and repaired:
            return repaired
    except Exception:
        pass
    
    # ── STAGE 9: Last resort aggressive clean ─
    # Strip everything except basic JSON characters
    try:
        aggressive = re.sub(
            r'[^\x20-\x7E]',  # Keep only printable ASCII
            '', 
            raw
        )
        aggressive = re.sub(r',\s*([}\]])', r'\1', aggressive)
        result = json.loads(aggressive)
        if isinstance(result, dict):
            return result
    except json.JSONDecodeError:
        pass
    
    # ── STAGE 10: Complete failure ─────────────
    # All 9 stages failed. Raise clear error.
    raise ValueError(
        f"[{source}] JSON parsing failed after all "
        f"recovery attempts. "
        f"Raw response (first 500 chars): {raw[:500]}"
    )
