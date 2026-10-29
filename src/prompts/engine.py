"""Advanced Prompt Engineering Engine with structured templates and persona adaptation."""
from typing import Any, Dict, List


class PromptEngine:
    """Manages prompt engineering best practices: role framing, few-shot examples, and strict constraints."""

    SYSTEM_ROLE = """You are an Enterprise Forward-Deployed AI Agent acting on behalf of AppXcelerate Solutions.
Your goal is to solve customer inquiries by coordinating with internal enterprise tools (CRM, SQL Database, Webhooks).

Follow these strict rules:
1. Ground every claim on returned tool outputs. Never invent fake order IDs, account balances, or SLAs.
2. For financial actions or refunds exceeding the approved threshold, request Human-In-The-Loop approval.
3. Output all final responses in structured, concise, client-ready language.
"""

    @classmethod
    def format_plan_prompt(cls, user_intent: str, available_tools: List[str]) -> str:
        tools_str = ", ".join(available_tools)
        return f"""Customer Request: "{user_intent}"
Available Tools: [{tools_str}]

Determine the optimal step-by-step execution plan. Select the first tool to invoke and specify the required parameters."""

    @classmethod
    def format_synthesis_prompt(cls, user_intent: str, tool_observations: List[Dict[str, Any]]) -> str:
        obs_summary = "\n".join([f"- Action {o.get('action')}: {o.get('result')}" for o in tool_observations])
        return f"""User Inquiry: {user_intent}
Tool Execution Observations:
{obs_summary}

Synthesize a professional, empathetic, and definitive resolution for the client."""
