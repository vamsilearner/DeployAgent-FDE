"""Agent Execution Planner coordinating tools, HITL safety, and telemetry."""
import time
from typing import Any, Dict, List
from ..tools.crm_tool import CRMTool
from ..tools.database_tool import DatabaseTool
from ..tools.webhook_tool import WebhookTool
from ..telemetry.tracer import TelemetryTracer
from .hitl import HumanInTheLoopGate


class ForwardDeployedAgent:
    """The Forward Deployed Agent orchestrating customer workflows."""

    def __init__(self):
        self.crm = CRMTool()
        self.db = DatabaseTool()
        self.webhook = WebhookTool()
        self.hitl = HumanInTheLoopGate()

    def process_customer_request(self, customer_id: str, request_text: str, session_id: str = "sess-001") -> Dict[str, Any]:
        tracer = TelemetryTracer(session_id=session_id, client_id=customer_id)
        observations: List[Dict[str, Any]] = []

        # Step 1: CRM Profile Lookup
        t0 = time.perf_counter()
        crm_res = self.crm.execute(action="lookup_customer", customer_id=customer_id)
        duration = (time.perf_counter() - t0) * 1000
        tracer.record_trace("crm_lookup", "CRMTool", duration, {"customer_id": customer_id})
        tracer.add_tokens(180)

        if crm_res.get("status") != "success":
            return {
                "status": "failed",
                "message": f"Customer validation failed: {crm_res.get('message')}",
                "telemetry": tracer.get_summary()
            }

        client_name = crm_res["data"]["name"]
        observations.append({"action": "crm_lookup", "result": f"Verified {client_name} (Tier: {crm_res['data']['tier']})"})

        # Step 2: Intent-driven Tool Dispatch
        req_lower = request_text.lower()

        # Branch A: Order or Deployment Status Inquiry
        if "order" in req_lower or "gpu" in req_lower or "storage" in req_lower or "status" in req_lower:
            t0 = time.perf_counter()
            db_res = self.db.execute(query_type="SELECT", filter_field="customer_id", filter_value=customer_id)
            duration = (time.perf_counter() - t0) * 1000
            tracer.record_trace("database_query", "DatabaseTool", duration, {"filter": customer_id})
            tracer.add_tokens(240)

            rows = db_res.get("rows", [])
            observations.append({"action": "sql_query", "result": f"Retrieved {len(rows)} active operational orders"})

            # Generate grounded client response
            order_details = "; ".join([f"{r['item']} ({r['status']})" for r in rows]) if rows else "No active orders found"
            resolution = f"Hello {client_name}, our operational telemetry confirms your current orders: {order_details}."

        # Branch B: Credit / Refund Request
        elif "refund" in req_lower or "credit" in req_lower:
            # Extract requested amount heuristically or default to $150
            amount = 150.0
            if "$300" in req_lower or "300" in req_lower:
                amount = 300.0

            payload = {"amount": amount}
            gate_check = self.hitl.inspect_action("apply_credit", payload)

            if gate_check["requires_approval"]:
                # Trigger Webhook Alert to Client Manager
                self.webhook.execute(channel="cs-escalations", message=f"Approval needed: {client_name} requested ${amount} credit.", severity="HIGH")
                resolution = f"Hello {client_name}, your credit request for ${amount:.2f} has been submitted and escalated to your Dedicated Success Manager for approval."
                observations.append({"action": "hitl_escalation", "result": gate_check["reason"]})
            else:
                self.crm.execute(action="apply_credit", customer_id=customer_id, payload=payload)
                resolution = f"Hello {client_name}, a credit of ${amount:.2f} has been automatically applied to your account."
                observations.append({"action": "auto_credit", "result": f"${amount} credited successfully"})

        # Branch C: General Ticket Creation
        else:
            self.crm.execute(action="create_ticket", customer_id=customer_id, payload={"subject": request_text, "priority": "P2"})
            resolution = f"Hello {client_name}, we have logged your inquiry into our engineering ticketing system under Priority 2."
            observations.append({"action": "create_ticket", "result": "Ticket created"})

        return {
            "status": "completed",
            "resolution": resolution,
            "observations": observations,
            "telemetry": tracer.get_summary()
        }
