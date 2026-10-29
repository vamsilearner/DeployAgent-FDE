"""Pydantic schemas for FDE API Gateway."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    customer_id: str = Field(..., example="CUST-101")
    request_text: str = Field(..., example="What is the current status of my dedicated GPU pod order?")
    session_id: Optional[str] = Field(default="sess-default")


class AgentRunResponse(BaseModel):
    status: str
    resolution: str
    observations: List[Dict[str, Any]]
    telemetry: Dict[str, Any]
