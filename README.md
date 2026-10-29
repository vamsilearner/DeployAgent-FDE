# DeployAgent-FDE: Enterprise Forward-Deployed AI Agent & Workflow Platform

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Tests Passing](https://img.shields.io/badge/PyTest-Passing-success)](tests/)

**DeployAgent-FDE** is a production-grade Forward-Deployed AI Agent platform tailored for enterprise customer onboarding, CRM/ERP tool orchestration, and automated workflow resolution. Built specifically to demonstrate Forward Deployed Engineering (FDE) capabilities in Generative AI, it bridges customer software with LLM tool-calling orchestration.

---

## Architecture Flow

```mermaid
flowchart TD
    Client[Enterprise Customer Request] --> Gateway[FastAPI Customer Gateway]
    Gateway --> Planner[Forward Deployed Agent Planner]
    
    Planner --> CRM[CRM Tool: Profile & Tickets]
    Planner --> SQL[SQL Tool: Safe Read-Only Queries]
    Planner --> Webhook[Webhook Dispatcher: Slack/Teams Alerts]
    
    Planner --> HITL{Human-in-the-Loop Threshold Check}
    HITL -->|Refund > $250| Escalate[Escalate to Customer Success Manager]
    HITL -->|Safe Transaction| AutoExecute[Execute Auto-Action & Update CRM]
    
    Planner --> Telemetry[Telemetry Engine: Latency, Tokens & Cost Tracking]
    Planner --> Response[Structured Client Resolution]
```

---

## Key Engineering Capabilities
1. **Multi-Tool Orchestration**: Seamless integration with CRM (Salesforce/HubSpot model), read-only SQL operational databases, and asynchronous Webhook alerting.
2. **Human-in-the-Loop (HITL) Policy Gates**: High-risk financial operations automatically trigger supervisor escalation while low-risk inquiries resolve instantly.
3. **Enterprise Telemetry & Observability**: Real-time token usage, per-session dollar cost tracking, and execution tracing.
4. **Resilience & Circuit Breaker**: Fallback model routing and safe error handling.

---

## Quickstart Guide

```bash
# Install dependencies
pip install -r requirements.txt

# Run unit tests
python3 -m unittest discover -s tests -p "test_*.py" -v

# Run interactive customer integration demo
python3 scripts/run_fde_demo.py

# Start API service
uvicorn src.api.app:app --host 0.0.0.0 --port 8001 --reload
```
