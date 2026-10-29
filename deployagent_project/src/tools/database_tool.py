"""Safe SQL / Database connector tool with read-only validation."""
from typing import Any, Dict, List
from .base import BaseTool


class DatabaseTool(BaseTool):
    """Executes safe customer database queries for order status, telemetry, and product inventory."""

    name = "sql_data_connector"
    description = "Queries enterprise operational databases for transaction records, invoices, and shipment tracking."

    ORDERS_TABLE = [
        {"order_id": "ORD-501", "customer_id": "CUST-101", "item": "Dedicated GPU Pod", "status": "DELIVERED", "amount": 4200.0},
        {"order_id": "ORD-502", "customer_id": "CUST-101", "item": "Cold Storage Volume 10TB", "status": "PROVISIONING", "amount": 800.0},
        {"order_id": "ORD-503", "customer_id": "CUST-102", "item": "Standard Inference API Pack", "status": "ACTIVE", "amount": 350.0},
    ]

    def execute(self, query_type: str, filter_field: str, filter_value: Any) -> Dict[str, Any]:
        # Safety check: prevent arbitrary mutations or SQL injections
        if query_type != "SELECT":
            return {"status": "error", "message": "Security Violation: Database connector is strictly READ-ONLY (SELECT allowed)."}

        results = []
        for row in self.ORDERS_TABLE:
            if str(row.get(filter_field, "")).lower() == str(filter_value).lower():
                results.append(row)

        return {
            "status": "success",
            "row_count": len(results),
            "rows": results
        }
