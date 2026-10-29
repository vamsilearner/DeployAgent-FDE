"""Telemetry, latency timing, token cost calculation, and audit logging."""
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List
from ..core.config import settings


@dataclass
class ExecutionTrace:
    action_type: str
    component: str
    duration_ms: float
    details: Dict[str, Any] = field(default_factory=dict)


class TelemetryTracer:
    """Tracks token consumption, dollar costs, and latency across FDE agent customer sessions."""

    def __init__(self, session_id: str, client_id: str):
        self.session_id = session_id
        self.client_id = client_id
        self.start_time = time.perf_counter()
        self.traces: List[ExecutionTrace] = []
        self.total_tokens: int = 0
        self.estimated_cost_usd: float = 0.0

    def record_trace(self, action_type: str, component: str, duration_ms: float, details: Dict[str, Any] = None):
        self.traces.append(
            ExecutionTrace(
                action_type=action_type,
                component=component,
                duration_ms=round(duration_ms, 2),
                details=details or {},
            )
        )

    def add_tokens(self, tokens: int, model: str = "gpt-4o"):
        self.total_tokens += tokens
        price_per_1k = settings.model_pricing.get(model, 0.005)
        self.estimated_cost_usd += (tokens / 1000.0) * price_per_1k

    def get_summary(self) -> Dict[str, Any]:
        total_duration_ms = (time.perf_counter() - self.start_time) * 1000
        return {
            "session_id": self.session_id,
            "client_id": self.client_id,
            "total_duration_ms": round(total_duration_ms, 2),
            "total_tokens": self.total_tokens,
            "estimated_cost_usd": round(self.estimated_cost_usd, 5),
            "step_count": len(self.traces),
            "trace_details": [
                {"action": t.action_type, "component": t.component, "duration_ms": t.duration_ms}
                for t in self.traces
            ]
        }
