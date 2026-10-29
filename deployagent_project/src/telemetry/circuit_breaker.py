"""Resilience circuit breaker and multi-model fallback router."""
from typing import Any, Callable, Dict
from ..core.config import settings


class CircuitBreaker:
    """Safeguards customer integrations against primary API provider timeouts and outages."""

    def __init__(self, failure_threshold: int = 3):
        self.failure_threshold = failure_threshold
        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call_with_fallback(self, primary_func: Callable, fallback_func: Callable, *args, **kwargs) -> Dict[str, Any]:
        if self.state == "OPEN":
            # Direct fallback
            return fallback_func(*args, **kwargs)

        try:
            res = primary_func(*args, **kwargs)
            self.failure_count = 0
            return res
        except Exception as e:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            # Execute fallback immediately
            return fallback_func(*args, **kwargs)
