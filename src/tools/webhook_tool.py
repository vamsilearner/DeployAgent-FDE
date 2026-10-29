"""Webhook and alert notification tool."""
from typing import Any, Dict
from .base import BaseTool


class WebhookTool(BaseTool):
    """Dispatches asynchronous webhooks to Slack, Microsoft Teams, or client webhook endpoints."""

    name = "webhook_dispatcher"
    description = "Sends urgent notification payloads and escalation alerts to client Slack/Teams channels."

    def execute(self, channel: str, message: str, severity: str = "INFO") -> Dict[str, Any]:
        # Simulated webhook dispatcher
        return {
            "status": "success",
            "channel": channel,
            "dispatched": True,
            "severity": severity,
            "preview": message[:60] + "..." if len(message) > 60 else message
        }
