"""Unit tests for Forward Deployed Agent planning & HITL gates."""
import unittest
from src.agent.planner import ForwardDeployedAgent
from src.agent.hitl import HumanInTheLoopGate


class TestFDEAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ForwardDeployedAgent()

    def test_order_status_workflow(self):
        res = self.agent.process_customer_request("CUST-101", "What is the status of my GPU order?")
        self.assertEqual(res["status"], "completed")
        self.assertIn("Acme Corp", res["resolution"])
        self.assertIn("Dedicated GPU Pod", res["resolution"])
        self.assertGreater(res["telemetry"]["total_tokens"], 0)

    def test_hitl_escalation_on_large_refund(self):
        res = self.agent.process_customer_request("CUST-101", "I demand a $300 credit refund immediately.")
        self.assertEqual(res["status"], "completed")
        self.assertIn("escalated", res["resolution"].lower())

    def test_auto_credit_on_small_refund(self):
        res = self.agent.process_customer_request("CUST-101", "Please issue a $50 credit for downtime.")
        self.assertEqual(res["status"], "completed")
        self.assertIn("automatically applied", res["resolution"].lower())


if __name__ == "__main__":
    unittest.main()
