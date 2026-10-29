"""Base class for enterprise customer tools."""
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """Abstract base class for all tools callable by the Forward Deployed Agent."""

    name: str = "base_tool"
    description: str = "Description of the tool"

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool action."""
        pass

    def get_schema(self) -> Dict[str, Any]:
        """Return JSON schema describing the tool parameters."""
        return {
            "name": self.name,
            "description": self.description,
        }
