"""Configuration settings for DeployAgent FDE platform."""
import os
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class FDESettings:
    app_name: str = "DeployAgent FDE Platform"
    app_env: str = os.getenv("APP_ENV", "development")
    port: int = int(os.getenv("PORT", "8001"))

    # Models
    primary_model: str = os.getenv("PRIMARY_MODEL", "gpt-4o")
    fallback_model: str = os.getenv("FALLBACK_MODEL", "gpt-4o-mini")

    # Cost per 1K tokens ($)
    model_pricing: Dict[str, float] = field(default_factory=lambda: {
        "gpt-4o": 0.005,
        "gpt-4o-mini": 0.00015,
        "mock-model": 0.0,
    })

    # FDE Customer Policy Thresholds
    hitl_refund_threshold_usd: float = 250.0  # Above this, require human supervisor approval
    max_agent_steps: int = 5


settings = FDESettings()
