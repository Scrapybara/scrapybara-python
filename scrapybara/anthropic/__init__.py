from typing import Literal, Optional, List, TypedDict
from anthropic.types.beta import (
    BetaToolComputerUse20241022Param,
    BetaToolTextEditor20241022Param,
    BetaToolBash20241022Param,
)
import asyncio

from .base import BaseAnthropicTool, CLIResult, ToolError, ToolResult
from .. import Scrapybara

class ComputerToolOptions(TypedDict):
    display_height_px: int
    display_width_px: int
    display_number: int | None

class ComputerTool(BaseAnthropicTool):
    """
    A computer interaction tool that allows the agent to control mouse and keyboard.
    The tool parameters are defined by Anthropic and are not editable.
    """

    api_type: Literal["computer_20241022"] = "computer_20241022"
    name: Literal["computer"] = "computer"
    width: int = 1024
    height: int = 768
    display_num: int | None = 1

    def __init__(self, scrapybara: Scrapybara, instance_id: str):
        self.scrapybara = scrapybara
        self.instance_id = instance_id
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
            **self.options,
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
            # Parse the result dictionary
            return CLIResult(
                output=result.get('output', ''),
                error=result.get('error'),
                base64_image=result.get('base64_image'),
                system=result.get('system')
            )
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
                    file_text=file_text,
                    view_range=view_range,
                    old_str=old_str,
                    new_str=new_str,
                    insert_line=insert_line,
                ),
            )
            return CLIResult(
                output=result.get('output', ''),
                error=result.get('error'),
                base64_image=result.get('base64_image'),
                system=result.get('system')
            )
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
            return CLIResult(
                output=result.get('output', ''),
                error=result.get('error'),
                base64_image=result.get('base64_image'),
                system=result.get('system')
            )
        except Exception as e:
            raise ToolError(str(e)) from None
