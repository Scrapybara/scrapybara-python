from typing import Any, List, Optional, Tuple
from pydantic import BaseModel, Field

from ..types import Action, Button, ClickMouseActionClickType, Tool
from ..client import BaseInstance, UbuntuInstance
from ..instance.types import Command


class ComputerToolParameters(BaseModel):
    """Parameters for computer interaction commands."""

    action: Action = Field(description="The computer action to execute")
    button: Optional[Button] = Field(None, description="The button to click")
    click_type: Optional[ClickMouseActionClickType] = Field(
        None, description="The type of click to perform"
    )
    coordinates: Optional[List[int]] = Field(
        None, description="The coordinates to move to"
    )
    delta_x: Optional[float] = Field(None, description="The x delta to move")
    delta_y: Optional[float] = Field(None, description="The y delta to move")
    num_clicks: Optional[int] = Field(
        None, description="The number of clicks to perform"
    )
    hold_keys: Optional[List[str]] = Field(None, description="The keys to hold")
    path: Optional[List[List[int]]] = Field(None, description="The path to move to")
    keys: Optional[List[str]] = Field(None, description="The keys to press")
    text: Optional[str] = Field(None, description="The text to type")
    duration: Optional[float] = Field(None, description="The duration to wait")


class ComputerTool(Tool):
    """A computer interaction tool that allows the agent to control mouse and keyboard.

    Available for Ubuntu, Browser, and Windows instances."""

    _instance: BaseInstance

    def __init__(self, instance: BaseInstance) -> None:
        super().__init__(
            name="computer",
            description="Control mouse and keyboard for computer interaction",
            parameters=ComputerToolParameters,
        )
        self._instance = instance

    def __call__(self, **kwargs: Any) -> Any:
        params = ComputerToolParameters.model_validate(kwargs)

        if params.action == "move_mouse":
            if not params.coordinates:
                raise ValueError("coordinates is required for move_mouse action")
            return self._instance.computer(
                action=params.action,
                coordinates=params.coordinates,
                hold_keys=params.hold_keys,
            )
        elif params.action == "click_mouse":
            if not params.button:
                raise ValueError("button is required for click_mouse action")
            return self._instance.computer(
                action=params.action,
                button=params.button,
                click_type=params.click_type,
                coordinates=params.coordinates,
                num_clicks=params.num_clicks,
                hold_keys=params.hold_keys,
            )
        elif params.action == "drag_mouse":
            if not params.path:
                raise ValueError("path is required for drag_mouse action")
            return self._instance.computer(
                action=params.action,
                path=params.path,
                hold_keys=params.hold_keys,
            )
        elif params.action == "scroll":
            return self._instance.computer(
                action=params.action,
                coordinates=params.coordinates,
                delta_x=params.delta_x,
                delta_y=params.delta_y,
                hold_keys=params.hold_keys,
            )
        elif params.action == "press_key":
            if not params.keys:
                raise ValueError("keys is required for press_key action")
            return self._instance.computer(
                action=params.action,
                keys=params.keys,
                duration=params.duration,
            )
        elif params.action == "type_text":
            if not params.text:
                raise ValueError("text is required for type_text action")
            return self._instance.computer(
                action=params.action,
                text=params.text,
                hold_keys=params.hold_keys,
            )
        elif params.action == "wait":
            if params.duration is None:
                raise ValueError("duration is required for wait action")
            return self._instance.computer(
                action=params.action,
                duration=params.duration,
            )
        elif params.action == "take_screenshot":
            return self._instance.computer(action=params.action)
        elif params.action == "get_cursor_position":
            return self._instance.computer(action=params.action)
        else:
            raise ValueError(f"Unknown action: {params.action}")


class EditToolParameters(BaseModel):
    """Parameters for file editing commands."""

    command: Command = Field(description="The edit command to execute")
    path: str = Field(description="Path to the file to edit")
    file_text: Optional[str] = Field(
        None, description="File content for create command"
    )
    view_range: Optional[Tuple[int, int]] = Field(
        None, description="Line range for view command"
    )
    old_str: Optional[str] = Field(
        None, description="String to replace for replace command"
    )
    new_str: Optional[str] = Field(None, description="New string for replace command")
    insert_line: Optional[int] = Field(
        None, description="Line number for insert command"
    )


class EditTool(Tool):
    """A filesystem editor tool that allows the agent to view, create, and edit files.

    Available for Ubuntu instances."""

    _instance: UbuntuInstance

    def __init__(self, instance: UbuntuInstance) -> None:
        super().__init__(
            name="str_replace_editor",
            description="View, create, and edit files in the filesystem",
            parameters=EditToolParameters,
        )
        self._instance = instance

    def __call__(self, **kwargs: Any) -> Any:
        params = EditToolParameters.model_validate(kwargs)
        return self._instance.edit(
            command=params.command,
            path=params.path,
            file_text=params.file_text,
            view_range=params.view_range,
            old_str=params.old_str,
            new_str=params.new_str,
            insert_line=params.insert_line,
        )


class BashToolParameters(BaseModel):
    """Parameters for bash command execution."""

    command: str = Field(description="The bash command to execute")
    restart: Optional[bool] = Field(False, description="Whether to restart the shell")


class BashTool(Tool):
    """A shell execution tool that allows the agent to run bash commands.

    Available for Ubuntu instances."""

    _instance: UbuntuInstance

    def __init__(self, instance: UbuntuInstance) -> None:
        super().__init__(
            name="bash",
            description="Execute bash commands in the shell",
            parameters=BashToolParameters,
        )
        self._instance = instance

    def __call__(self, **kwargs: Any) -> Any:
        params = BashToolParameters.model_validate(kwargs)
        return self._instance.bash(command=params.command, restart=params.restart)
