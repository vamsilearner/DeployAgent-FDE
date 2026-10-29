"""Unit tests for enterprise customer tools."""
import unittest
from src.tools.crm_tool import CRMTool
from src.tools.database_tool import DatabaseTool
from src.tools.webhook_tool import WebhookTool


class TestFDETools(unittest.TestCase):
    def setUp(self):
        self.crm = CRMTool()
        self.db = DatabaseTool()
        self.webhook = WebhookTool()

    def test_crm_lookup_success(self):
        res = self.crm.execute("lookup_customer", "CUST-101")
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["data"]["name"], "Acme Corp")

    def test_crm_lookup_invalid_user(self):
        res = self.crm.execute("lookup_customer", "CUST-999")
        self.assertEqual(res["status"], "error")

    def test_database_safe_select(self):
        res = self.db.execute("SELECT", "customer_id", "CUST-101")
        self.assertEqual(res["status"], "success")
        self.assertGreaterEqual(res["row_count"], 1)

    def test_database_blocks_mutation(self):
        res = self.db.execute("DROP TABLE", "customer_id", "CUST-101")
        self.assertEqual(res["status"], "error")
        self.assertIn("Security Violation", res["message"])

    def test_webhook_dispatch(self):
        res = self.webhook.execute("alerts", "Test alert message", "INFO")
        self.assertTrue(res["dispatched"])


if __name__ == "__main__":
    unittest.main()
