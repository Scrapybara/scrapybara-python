from typing import Any, Dict, Optional
from pydantic import BaseModel


class Tool(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

    def __call__(self, **kwargs: Any) -> Any:
        raise NotImplementedError("Tool.__call__ must be implemented by subclasses")
