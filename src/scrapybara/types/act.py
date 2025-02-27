from typing import Any, Dict, List, Literal, Optional, Union, Generic, TypeVar
from pydantic import BaseModel
from .tool import Tool, ApiTool  # noqa: F401

OutputT = TypeVar("OutputT")


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

class ReasoningPart(BaseModel):
    type: Literal["reasoning"] = "reasoning"
    reasoning: str
    signature: Optional[str] = None
    instructions: Optional[str] = None

class UserMessage(BaseModel):
    role: Literal["user"] = "user"
    content: List[Union[TextPart, ImagePart]]


class AssistantMessage(BaseModel):
    role: Literal["assistant"] = "assistant"
    content: List[Union[TextPart, ToolCallPart, ReasoningPart]]


class ToolMessage(BaseModel):
    role: Literal["tool"] = "tool"
    content: List[ToolResultPart]


Message = Union[UserMessage, AssistantMessage, ToolMessage]


# Request/Response models
class Model(BaseModel):
    provider: Literal["anthropic", "herd"]
    name: str
    api_key: Optional[str] = None


class SingleActRequest(BaseModel):
    model: Model
    system: Optional[str] = None
    messages: Optional[List[Message]] = None
    tools: Optional[List[ApiTool]] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class SingleActResponse(BaseModel):
    message: AssistantMessage
    finish_reason: Literal[
        "stop", "length", "content-filter", "tool-calls", "error", "other", "unknown"
    ]
    usage: Optional[TokenUsage] = None


# Step definition
class Step(BaseModel):
    text: str
    reasoning_parts: Optional[List[ReasoningPart]] = None
    tool_calls: Optional[List[ToolCallPart]] = None
    tool_results: Optional[List[ToolResultPart]] = None
    finish_reason: Optional[
        Literal[
            "stop",
            "length",
            "content-filter",
            "tool-calls",
            "error",
            "other",
            "unknown",
        ]
    ] = None
    usage: Optional[TokenUsage] = None


# Act response
class ActResponse(BaseModel, Generic[OutputT]):
    messages: List[Message]
    steps: List[Step]
    text: Optional[str] = None
    output: OutputT
    usage: Optional[TokenUsage] = None
