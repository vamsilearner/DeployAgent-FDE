"""Structured JSON output validator and self-healing schema repair."""
import json
import re
from typing import Any, Dict, Tuple


class SchemaValidator:
    """Validates that LLM completions conform to expected JSON schemas, with regex-based auto-repair."""

    @staticmethod
    def extract_json(raw_text: str) -> Tuple[bool, Dict[str, Any]]:
        """Extracts JSON object even if wrapped in markdown codeblocks or conversational filler."""
        if not raw_text:
            return False, {}

        # 1. Direct parse attempt
        try:
            return True, json.loads(raw_text)
        except json.JSONDecodeError:
            pass

        # 2. Extract from markdown code fence ```json ... ```
        fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
        if fence_match:
            try:
                return True, json.loads(fence_match.group(1))
            except json.JSONDecodeError:
                pass

        # 3. Fallback: regex search for outer braces
        brace_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if brace_match:
            try:
                return True, json.loads(brace_match.group(0))
            except json.JSONDecodeError:
                pass

        return False, {"raw_output": raw_text}
