"""
utils/cerebras.py — Cerebras Cloud SDK client for Reponify.

Single LLM provider for all pipeline layers:
  VISION   (llama3.1-8b)   → Layer 1
  CREATIVE (gpt-oss-120b)  → Layer 2

Key rotation: immediate rotate on any server/rate-limit error.
No retry on the same key. Rotate instantly.
"""

import json
import re

from cerebras.cloud.sdk import Cerebras
from config import settings
from utils.json_cleaner import clean_and_parse


class CerebrasRotator:
    def __init__(self):
        self._keys = settings.cerebras_api_keys
        self._index = 0

    def _get_client(self, key_index: int) -> Cerebras:
        return Cerebras(api_key=self._keys[key_index])

    def call(self, prompt: str, model: str,
             system: str = None, max_tokens: int = None) -> dict:

        total_keys = len(self._keys)
        recovery_attempts = 0

        for attempt in range(total_keys):
            current_index = (self._index + attempt) % total_keys

            while True:
                try:
                    client = self._get_client(current_index)

                    messages = []
                    if system:
                        messages.append({
                            "role": "system",
                            "content": system
                        })
                    messages.append({
                        "role": "user",
                        "content": prompt
                    })

                    kwargs = {
                        "model": model,
                        "messages": messages,
                        "temperature": 0.3,
                    }
                    if max_tokens:
                        kwargs["max_tokens"] = max_tokens
                        
                    response = client.chat.completions.create(**kwargs)

                    raw = response.choices[0].message.content

                    # Update index to current working key
                    self._index = current_index

                    return clean_and_parse(raw, source="Cerebras")

                except Exception as e:
                    error_str = str(e).lower()

                    # Universal auto-recovery for Context Length Exceeded (Family of errors)
                    if any(err in error_str for err in ["context_length_exceeded", "reduce the length", "maximum context", "context length", "too long"]):
                        if recovery_attempts < 4:
                            recovery_attempts += 1
                            print(f"[Cerebras] Context length exceeded. Auto-truncating prompt to fit (Recovery {recovery_attempts}/4)...")
                            if max_tokens and max_tokens > 1024:
                                max_tokens = int(max_tokens * 0.75) # Reduce completion tokens to give prompt more room
                            else:
                                # Cut out the middle 20% of the prompt, keeping the important start and end
                                plen = len(prompt)
                                keep = int(plen * 0.4)
                                prompt = prompt[:keep] + "\n\n...[TRUNCATED TO FIT CONTEXT LIMIT]...\n\n" + prompt[-keep:]
                            continue # Retry immediately on the same key
                        else:
                            raise RuntimeError(f"[cerebras] Context length exceeded even after 4 auto-truncation recoveries: {str(e)}")

                    # Check if this is a rate limit /
                    # server side error worth rotating on
                    should_rotate = any(term in error_str for term in [
                        "429",
                        "rate limit",
                        "rate_limit",
                        "quota",
                        "resource_exhausted",
                        "too many requests",
                        "503",
                        "502",
                        "500",
                        "server error",
                        "overloaded",
                    ])

                    if should_rotate:
                        print(f"[Cerebras] Server error on key "
                              f"{current_index + 1}. "
                              f"Rotating immediately to key "
                              f"{((current_index + 1) % total_keys) + 1}")
                        break  # Break while loop to continue to next key attempt

                    else:
                        # Non-rotatable error
                        raise RuntimeError(
                            f"[cerebras] Non-rotatable error "
                            f"on key {current_index + 1}: {str(e)}"
                        )

        # All 4 keys exhausted
        raise RuntimeError(
            "[cerebras] All 4 API keys exhausted. "
            "Rate limits hit on every key. "
            "Try again later."
        )





# Single global instance
cerebras_rotator = CerebrasRotator()


# Clean public functions for each layer
def call_vision(prompt: str, system: str) -> dict:
    return cerebras_rotator.call(
        prompt=prompt,
        model=settings.CEREBRAS_VISION_MODEL,
        system=system,
        max_tokens=4096,
    )

def call_creative(prompt: str, system: str) -> dict:
    return cerebras_rotator.call(
        prompt=prompt,
        model=settings.CEREBRAS_CREATIVE_MODEL,
        system=system,
        max_tokens=4096,
    )
