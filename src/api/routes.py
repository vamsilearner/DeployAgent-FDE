"""FastAPI routes for Forward Deployed Agent Gateway."""
from fastapi import APIRouter, HTTPException
from .schemas import AgentRunRequest, AgentRunResponse
from ..agent.planner import ForwardDeployedAgent

router = APIRouter()
agent_instance = ForwardDeployedAgent()


@router.get("/health")
def health():
    return {"status": "healthy", "service": "DeployAgent-FDE Gateway", "version": "1.0.0"}


@router.post("/agent/execute", response_model=AgentRunResponse)
def execute_agent(payload: AgentRunRequest):
    try:
        res = agent_instance.process_customer_request(
            customer_id=payload.customer_id,
            request_text=payload.request_text,
            session_id=payload.session_id or "sess-web"
        )
        return AgentRunResponse(**res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
