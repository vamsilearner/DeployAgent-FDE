"""Interactive CLI demo for the Forward Deployed Engineer Agent."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.planner import ForwardDeployedAgent


def main():
    print("=" * 65)
    print(" DeployAgent-FDE: Enterprise Customer Integration Platform")
    print(" AppXcelerate Solutions - Forward Deployed Engineer Demo")
    print("=" * 65)

    agent = ForwardDeployedAgent()
    scenarios = [
        ("CUST-101", "Can you check the current provisioning status of my GPU pod and storage?"),
        ("CUST-101", "We experienced downtime during migration. Requesting a $300 service credit."),
        ("CUST-102", "We need a $50 adjustment on our current monthly invoice balance."),
    ]

    for cust_id, req in scenarios:
        print(f"\n[Customer: {cust_id}] Query: \"{req}\"")
        res = agent.process_customer_request(cust_id, req)
        print(f"[Agent Resolution]: {res['resolution']}")
        print(f"[Observations]: {res['observations']}")
        print(f"[Telemetry]: Duration={res['telemetry']['total_duration_ms']}ms | Tokens={res['telemetry']['total_tokens']} | Cost=${res['telemetry']['estimated_cost_usd']}")
        print("-" * 65)


if __name__ == "__main__":
    main()
