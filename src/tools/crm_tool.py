"""Mock Enterprise CRM Tool (Salesforce / HubSpot style connector)."""
from typing import Any, Dict, Optional
from .base import BaseTool


class CRMTool(BaseTool):
    """Interacts with customer relationship management database to look up accounts, update tickets, and issue credits."""

    name = "crm_connector"
    description = "Lookup customer profile, fetch open support tickets, and update account notes or status."

    # In-memory mock database of enterprise clients
    DB = {
        "CUST-101": {
            "name": "Acme Corp",
            "tier": "Enterprise",
            "mrr": 12500,
            "open_tickets": [
                {"ticket_id": "TICK-801", "subject": "API Rate limit exceeded on batch sync", "status": "OPEN", "priority": "P1"}
            ],
            "balance_due": 0.0
        },
        "CUST-102": {
            "name": "FinTech Global",
            "tier": "Scale",
            "mrr": 4500,
            "open_tickets": [],
            "balance_due": 350.0
        }
    }

    def execute(self, action: str, customer_id: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = payload or {}
        if customer_id not in self.DB:
            return {"status": "error", "message": f"Customer ID {customer_id} not found in CRM."}

        cust = self.DB[customer_id]

        if action == "lookup_customer":
            return {
                "status": "success",
                "customer_id": customer_id,
                "data": cust
            }

        elif action == "create_ticket":
            subject = payload.get("subject", "General Inbound Request")
            priority = payload.get("priority", "P2")
            new_id = f"TICK-{len(cust['open_tickets']) + 900}"
            cust["open_tickets"].append({"ticket_id": new_id, "subject": subject, "status": "OPEN", "priority": priority})
            return {"status": "success", "ticket_id": new_id, "message": "Ticket created in CRM"}

        elif action == "apply_credit":
            amount = float(payload.get("amount", 0.0))
            cust["balance_due"] = max(0.0, cust["balance_due"] - amount)
            return {"status": "success", "credited_amount": amount, "new_balance": cust["balance_due"]}

        return {"status": "error", "message": f"Unsupported CRM action: {action}"}
