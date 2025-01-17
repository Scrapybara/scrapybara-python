from typing import Any, Dict, Optional, Type
from pydantic import BaseModel


class Tool(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Optional[Type[BaseModel]] = None

    def __call__(self, **kwargs: Any) -> Any:
        """Execute the tool with the given arguments.

        The kwargs type will be inferred from the parameters field's type hints.
        """
        raise NotImplementedError("Tool.__call__ must be implemented by subclasses")


class ApiTool(BaseModel):
    """A tool that can be serialized to JSON for API calls."""

    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

    @classmethod
    def from_tool(cls, tool: Tool) -> "ApiTool":
        """Convert a Tool to an ApiTool for API serialization."""
        return cls(
            name=tool.name,
            description=tool.description,
            parameters=tool.parameters.model_json_schema() if tool.parameters else None,
        )
