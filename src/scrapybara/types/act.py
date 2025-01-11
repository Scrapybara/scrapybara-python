from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel


# Message part types
class TextPart(BaseModel):
    type: Literal["text"] = "text"
    text: str


class ImagePart(BaseModel):
    type: Literal["image"] = "image"
    image: str  # Base64 encoded image or URL
    mime_type: Optional[str] = None


class ToolCallPart(BaseModel):
    type: Literal["tool-call"] = "tool-call"
    tool_call_id: str
    tool_name: str
    args: Dict[str, Any]


class ToolResultPart(BaseModel):
    type: Literal["tool-result"] = "tool-result"
    tool_call_id: str
    tool_name: str
    result: Any
    is_error: Optional[bool] = False


class UserMessage(BaseModel):
    role: Literal["user"] = "user"
    content: List[Union[TextPart, ImagePart]]


class AssistantMessage(BaseModel):
    role: Literal["assistant"] = "assistant"
    content: List[Union[TextPart, ToolCallPart]]


class ToolMessage(BaseModel):
    role: Literal["tool"] = "tool"
    content: List[ToolResultPart]


Message = Union[UserMessage, AssistantMessage, ToolMessage]


# Tool definition
class Tool(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

    def __call__(self, **kwargs: Any) -> Any:
        raise NotImplementedError("Tool.__call__ must be implemented by subclasses")


# Request/Response models
class Model(BaseModel):
    provider: Literal["anthropic"]
    name: str
    api_key: Optional[str] = None


class ActRequest(BaseModel):
    model: Model
    system: Optional[str] = None
    messages: Optional[List[Message]] = None
    tools: Optional[List[Tool]] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ActResponse(BaseModel):
    message: AssistantMessage
    finish_reason: Literal[
        "stop", "length", "content-filter", "tool-calls", "error", "other", "unknown"
    ]
    usage: Optional[TokenUsage] = None


# Step definition
class Step(BaseModel):
    text: str
    tool_calls: Optional[List[ToolCallPart]] = None
    tool_results: Optional[List[ToolResultPart]] = None
    finish_reason: Optional[str] = Literal[
        "stop", "length", "content-filter", "tool-calls", "error", "other", "unknown"
    ]
    usage: Optional[TokenUsage] = None