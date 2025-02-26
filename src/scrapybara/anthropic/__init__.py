from typing import Literal, Optional, TypedDict, Any, Dict
from anthropic.types.beta import (
    BetaToolComputerUse20241022Param,
    BetaToolTextEditor20241022Param,
    BetaToolBash20241022Param,
)
import asyncio
from pydantic import Field

from ..client import BaseInstance, UbuntuInstance
from ..types.act import Model
from .base import BaseAnthropicTool, CLIResult, ToolError, ToolResult


# New: universal act API
class Anthropic(Model):
    """Model adapter for Anthropic.

    Supported models:
    - claude-3-7-sonnet-20250219 (1x agent credit if no api_key)
    - claude-3-7-sonnet-20250219-thinking (1x agent credit if no api_key)
    - claude-3-5-sonnet-20241022 (1x agent credit if no api_key)

    Args:
        name: Anthropic model name, defaults to "claude-3-7-sonnet-20250219"
        api_key: Optional Anthropic API key

    Returns:
        A Model configuration object
    """

    provider: Literal["anthropic"] = Field(default="anthropic", frozen=True)

    def __init__(
        self,
        name: Optional[str] = "claude-3-7-sonnet-20250219",
        api_key: Optional[str] = None,
    ) -> None:
        super().__init__(provider="anthropic", name=name, api_key=api_key)


# Legacy: Anthropic SDK-compatible tools
class ComputerToolOptions(TypedDict):
    display_height_px: int
    display_width_px: int
    display_number: Optional[int]


class ComputerTool(BaseAnthropicTool):
    """A computer interaction tool that allows the agent to control mouse and keyboard.

    Available for Ubuntu, Browser, and Windows instances."""

    api_type: Literal["computer_20241022"] = "computer_20241022"
    name: Literal["computer"] = "computer"
    width: int = 1024
    height: int = 768
    display_num: Optional[int] = 1
    _instance: BaseInstance

    def __init__(self, instance: BaseInstance):
        self._instance = instance
        super().__init__()

    @property
    def options(self) -> ComputerToolOptions:
        return {
            "display_width_px": self.width,
            "display_height_px": self.height,
            "display_number": self.display_num,
        }

    def to_params(self) -> BetaToolComputerUse20241022Param:
        return {
            "name": self.name,
            "type": self.api_type,
            "display_width_px": self.width,
            "display_height_px": self.height,
            "display_number": self.display_num,
        }

    async def __call__(self, **kwargs: Any) -> ToolResult:
        action = kwargs.pop("action")
        coordinate = kwargs.pop("coordinate", None)
        text = kwargs.pop("text", None)

        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self._instance.computer(
                    action=action,
                    coordinate=tuple(coordinate) if coordinate else None,
                    text=text,
                ),
            )
            return CLIResult(
                output=result.get("output") if result else "",
                error=result.get("error") if result else None,
                base64_image=result.get("base64_image") if result else None,
                system=result.get("system") if result else None,
            )
        except Exception as e:
            raise ToolError(str(e)) from None


class EditTool(BaseAnthropicTool):
    """A filesystem editor tool that allows the agent to view, create, and edit files.

    Available for Ubuntu instances."""

    api_type: Literal["text_editor_20241022"] = "text_editor_20241022"
    name: Literal["str_replace_editor"] = "str_replace_editor"
    _instance: UbuntuInstance

    def __init__(self, instance: UbuntuInstance):
        self._instance = instance
        super().__init__()

    def to_params(self) -> BetaToolTextEditor20241022Param:
        return {
            "name": self.name,
            "type": self.api_type,
        }

    async def __call__(self, **kwargs: Any) -> ToolResult:
        command = kwargs.pop("command")
        path = kwargs.pop("path")
        file_text = kwargs.pop("file_text", None)
        view_range = kwargs.pop("view_range", None)
        old_str = kwargs.pop("old_str", None)
        new_str = kwargs.pop("new_str", None)
        insert_line = kwargs.pop("insert_line", None)
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self._instance.edit(
                    command=command,
                    path=path,
                    file_text=file_text,
                    view_range=view_range,
                    old_str=old_str,
                    new_str=new_str,
                    insert_line=insert_line,
                ),
            )
            return CLIResult(
                output=result.get("output") if result else "",
                error=result.get("error") if result else None,
                base64_image=result.get("base64_image") if result else None,
                system=result.get("system") if result else None,
            )
        except Exception as e:
            raise ToolError(str(e)) from None


class BashTool(BaseAnthropicTool):
    """A shell execution tool that allows the agent to run bash commands.

    Available for Ubuntu instances."""

    api_type: Literal["bash_20241022"] = "bash_20241022"
    name: Literal["bash"] = "bash"
    _instance: UbuntuInstance

    def __init__(self, instance: UbuntuInstance):
        self._instance = instance
        super().__init__()

    def to_params(self) -> BetaToolBash20241022Param:
        return {
            "name": self.name,
            "type": self.api_type,
        }

    async def __call__(self, **kwargs: Any) -> ToolResult:
        command = kwargs.pop("command")
        restart = kwargs.pop("restart", False)
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self._instance.bash(command=command, restart=restart),
            )
            return CLIResult(
                output=result.get("output") if result else "",
                error=result.get("error") if result else None,
                base64_image=result.get("base64_image") if result else None,
                system=result.get("system") if result else None,
            )
        except Exception as e:
            raise ToolError(str(e)) from None


class ToolCollection:
    """A collection of anthropic-defined tools."""

    def __init__(self, *tools):
        self.tools = tools
        self.tool_map = {tool.to_params()["name"]: tool for tool in tools}

    def to_params(self) -> list:
        return [tool.to_params() for tool in self.tools]

    async def run(self, *, name: str, tool_input: Dict[str, Any]) -> ToolResult:
        tool = self.tool_map.get(name)
        if not tool:
            return ToolResult(error=f"Tool {name} not found")
        try:
            r = await tool(**tool_input)
            return r if r else ToolResult()
        except Exception as e:
            print(f"Error running tool {name}: {e}")
            return ToolResult(error=str(e))
