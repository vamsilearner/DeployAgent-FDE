"""Human-In-The-Loop (HITL) Policy Enforcement."""
from typing import Any, Dict
from ..core.config import settings


class HumanInTheLoopGate:
    """Intercepts high-risk customer actions and enforces human approval."""

    @staticmethod
    def inspect_action(action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates whether an action requires human supervisor approval."""
        if action == "apply_credit":
            amount = float(payload.get("amount", 0.0))
            if amount > settings.hitl_refund_threshold_usd:
                return {
                    "requires_approval": True,
                    "reason": f"Credit amount (${amount:.2f}) exceeds auto-approval threshold (${settings.hitl_refund_threshold_usd:.2f})",
                    "status": "PENDING_HUMAN_APPROVAL"
                }

        if action == "delete_account" or action == "purge_data":
            return {
                "requires_approval": True,
                "reason": "Irreversible data deletion action requires authorized executive approval",
                "status": "PENDING_HUMAN_APPROVAL"
            }

        return {"requires_approval": False, "status": "APPROVED"}
