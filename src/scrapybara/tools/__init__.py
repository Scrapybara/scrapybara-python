from typing import Any, List, Optional
from pydantic import BaseModel, Field

from ..types import Action, Button, ClickMouseActionClickType, Tool
from ..client import BaseInstance, UbuntuInstance
from ..instance.types import Command
from typing import Literal

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
    view_range: Optional[List[int]] = Field(
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

    command: Optional[str] = Field(description="The bash command to execute")
    restart: Optional[bool] = Field(False, description="Whether to restart the shell")
    get_background_processes: Optional[bool] = Field(None, description="Retrieve information (pid, status, command) about background processes")
    kill_pid: Optional[int] = Field(None, description="Process ID to kill")


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
        return self._instance.bash(
            command=params.command, 
            restart=params.restart,
            get_background_processes=params.get_background_processes,
            kill_pid=params.kill_pid
        )


class FilesystemToolParameters(BaseModel):
    """Parameters for filesystem operations."""

    command: Literal[
        "read", "write", "append", "delete", "exists", "list", "mkdir", "rmdir", "move", "copy",
        "view", "create", "replace", "insert", "delete_lines", "undo", "grep"
    ] = Field(
        description="The filesystem command to execute. Determines which other parameters are required or optional. Supported commands: read, write, append, delete, exists, list, mkdir, rmdir, move, copy, view, create, replace, insert, delete_lines, undo, grep."
    )
    
    path: Optional[str] = Field(
        None,
        description="Path to the file or directory. Required for commands: read, write, append, delete, exists, list, mkdir, rmdir, view, create, replace, insert, delete_lines, undo, grep."
    )
    
    content: Optional[str] = Field(
        None,
        description="Content to write, append, or create in a file. Required for commands: write, append, create."
    )
    
    mode: Optional[str] = Field(
        None,
        description="Mode for file operations ('text' or 'binary'). Optional for commands: read, write, append, create. Defaults to 'text' if not specified."
    )
    
    encoding: Optional[str] = Field(
        None,
        description="Encoding for text operations (e.g., 'utf-8'). Optional for commands: read, write, append, create. Defaults to 'utf-8' if not specified."
    )
    
    view_range: Optional[List[int]] = Field(
        None,
        description="Range of lines to view as [start, end]. Optional for command: view. Not applicable if viewing a directory."
    )
    
    recursive: Optional[bool] = Field(
        None,
        description="Whether to perform the operation recursively. Optional for command: delete (defaults to False); required to be True for grep when searching directories."
    )
    
    src: Optional[str] = Field(
        None,
        description="Source path for move and copy operations. Required for commands: move, copy."
    )
    
    dst: Optional[str] = Field(
        None,
        description="Destination path for move and copy operations. Required for commands: move, copy."
    )
    
    old_str: Optional[str] = Field(
        None,
        description="String to be replaced in the file. Required for command: replace."
    )
    
    new_str: Optional[str] = Field(
        None,
        description="Replacement string. Required for command: replace."
    )
    
    line: Optional[int] = Field(
        None,
        description="Line number where text should be inserted (1-based index). Required for command: insert."
    )
    
    text: Optional[str] = Field(
        None,
        description="Text to insert at the specified line. Required for command: insert."
    )
    
    lines: Optional[List[int]] = Field(
        None,
        description="List of line numbers to delete (1-based indices). Required for command: delete_lines."
    )
    
    all_occurrences: Optional[bool] = Field(
        None,
        description="Whether to replace all occurrences of old_str. Optional for command: replace. Defaults to False, replacing only the first occurrence."
    )
    
    pattern: Optional[str] = Field(
        None,
        description="Regex pattern to search for in files. Required for command: grep."
    )
    
    case_sensitive: Optional[bool] = Field(
        None,
        description="Whether the grep search is case-sensitive. Optional for command: grep. Defaults to True."
    )
    
    line_numbers: Optional[bool] = Field(
        None,
        description="Whether to include line numbers in grep output. Optional for command: grep. Defaults to True."
    )


class FilesystemTool(Tool):
    """A filesystem manipulation tool that allows the agent to perform various filesystem operations.

    Available for Ubuntu instances."""

    _instance: UbuntuInstance

    def __init__(self, instance: UbuntuInstance) -> None:
        super().__init__(
            name="filesystem",
            description="Perform filesystem operations like reading, writing, and manipulating files",
            parameters=FilesystemToolParameters,
        )
        self._instance = instance

    def __call__(self, **kwargs: Any) -> Any:
        params = FilesystemToolParameters.model_validate(kwargs)
        return self._instance.filesystem(
            command=params.command,
            path=params.path,
            content=params.content,
            mode=params.mode,
            encoding=params.encoding,
            view_range=params.view_range,
            recursive=params.recursive,
            src=params.src,
            dst=params.dst,
            old_str=params.old_str,
            new_str=params.new_str,
            line=params.line,
            text=params.text,
            lines=params.lines,
            all_occurrences=params.all_occurrences,
            pattern=params.pattern,
            case_sensitive=params.case_sensitive,
            line_numbers=params.line_numbers,
        )
