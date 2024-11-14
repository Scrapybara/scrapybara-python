from typing import Any, Literal, Optional, List, Dict
from anthropic.types.beta import (
    BetaToolComputerUse20241022Param,
    BetaToolTextEditor20241022Param,
    BetaToolBash20241022Param,
    BetaToolUnionParam,
)
import asyncio

from .base import BaseAnthropicTool, CLIResult, ToolError, ToolFailure, ToolResult
from .. import Scrapybara


class ToolCollection:
    """A collection of anthropic-defined tools."""

    def __init__(self, *tools: BaseAnthropicTool):
        self.tools = tools
        self.tool_map = {tool.to_params()["name"]: tool for tool in tools}

    def to_params(
        self,
    ) -> list[BetaToolUnionParam]:
        return [tool.to_params() for tool in self.tools]

    async def run(self, *, name: str, tool_input: dict[str, Any]) -> ToolResult:
        tool = self.tool_map.get(name)
        if not tool:
            return ToolFailure(error=f"Tool {name} is invalid")
        try:
            return await tool(**tool_input)
        except ToolError as e:
            return ToolFailure(error=e.message)


class ComputerTool(BaseAnthropicTool):
    """
    A computer interaction tool that allows the agent to control mouse and keyboard.
    The tool parameters are defined by Anthropic and are not editable.
    """

    api_type: Literal["computer_20241022"] = "computer_20241022"
    name: Literal["computer"] = "computer"

    def __init__(self, scrapybara: Scrapybara, instance_id: str):
        self.scrapybara = scrapybara
        self.instance_id = instance_id
        super().__init__()

    def to_params(self) -> BetaToolComputerUse20241022Param:
        return {
            "name": self.name,
            "type": self.api_type,
        }

    async def __call__(
        self,
        *,
        action: str,
        coordinate: Optional[List[int]] = None,
        text: Optional[str] = None,
        **kwargs,
    ) -> ToolResult:
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.scrapybara.computer(
                    instance_id=self.instance_id,
                    action=action,
                    coordinate=tuple(coordinate) if coordinate else None,
                    text=text,
                ),
            )
            return CLIResult(output=str(result))
        except Exception as e:
            raise ToolError(str(e)) from None


class EditTool(BaseAnthropicTool):
    """
    A filesystem editor tool that allows the agent to view, create, and edit files.
    The tool parameters are defined by Anthropic and are not editable.
    """

    api_type: Literal["text_editor_20241022"] = "text_editor_20241022"
    name: Literal["str_replace_editor"] = "str_replace_editor"

    def __init__(self, scrapybara: Scrapybara, instance_id: str):
        self.scrapybara = scrapybara
        self.instance_id = instance_id
        super().__init__()

    def to_params(self) -> BetaToolTextEditor20241022Param:
        return {
            "name": self.name,
            "type": self.api_type,
        }

    async def __call__(
        self,
        *,
        command: str,
        path: str,
        file_text: Optional[str] = None,
        view_range: Optional[List[int]] = None,
        old_str: Optional[str] = None,
        new_str: Optional[str] = None,
        insert_line: Optional[int] = None,
        **kwargs,
    ) -> ToolResult:
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.scrapybara.edit(
                    instance_id=self.instance_id,
                    command=command,
                    path=path,
                    content=file_text,
                    view_range=view_range,
                    old_text=old_str,
                    new_text=new_str,
                    line_number=insert_line,
                ),
            )
            return CLIResult(output=str(result))
        except Exception as e:
            raise ToolError(str(e)) from None


class BashTool(BaseAnthropicTool):
    """
    A shell execution tool that allows the agent to run bash commands.
    The tool parameters are defined by Anthropic and are not editable.
    """

    api_type: Literal["bash_20241022"] = "bash_20241022"
    name: Literal["bash"] = "bash"

    def __init__(self, scrapybara: Scrapybara, instance_id: str):
        self.scrapybara = scrapybara
        self.instance_id = instance_id
        super().__init__()

    def to_params(self) -> BetaToolBash20241022Param:
        return {
            "name": self.name,
            "type": self.api_type,
        }

    async def __call__(
        self,
        *,
        command: str,
        restart: bool = False,
        **kwargs,
    ) -> ToolResult:
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.scrapybara.bash(
                    instance_id=self.instance_id, command=command, restart=restart
                ),
            )
            return CLIResult(output=str(result))
        except Exception as e:
            raise ToolError(str(e)) from None
