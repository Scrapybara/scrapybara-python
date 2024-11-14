from typing import Optional, Dict, Any, List, Tuple, Literal
from enum import Enum
import base64
from dataclasses import dataclass
import requests
from datetime import datetime
import asyncio
import shlex
from pathlib import Path
from uuid import uuid4

Action = Literal[
    "key",
    "type",
    "mouse_move",
    "left_click",
    "left_click_drag",
    "right_click",
    "middle_click",
    "double_click",
    "screenshot",
    "cursor_position",
]

Command = Literal["view", "create", "str_replace", "insert", "undo_edit"]


class ScrapybaraError(Exception):
    """Base exception for Scrapybara SDK"""


class InstanceStatus(str, Enum):
    """
    Enumeration of possible instance states

    Attributes:
        DEPLOYING: Instance is being created and configured
        RUNNING: Instance is active and ready for use
        TERMINATED: Instance has been stopped
        ERROR: Instance encountered an error during operation
    """

    DEPLOYING = "deploying"
    RUNNING = "running"
    TERMINATED = "terminated"
    ERROR = "error"


@dataclass
class Instance:
    """
    Information about a virtual desktop instance

    Attributes:
        instance_id: Unique identifier for the instance
        public_ip: Public IP address of the instance
        status: Current status of the instance (InstanceStatus)
        launch_time: When the instance was started (optional)
    """

    instance_id: str
    public_ip: str
    status: InstanceStatus
    launch_time: Optional[datetime] = None


@dataclass
class ComputerAction:
    """
    Computer action data

    Attributes:
        action: Type of action to perform (see Action enum)
        coordinate: Optional (x, y) coordinates for mouse actions
        text: Optional text for keyboard actions
        keys: Optional keys for keyboard actions
    """

    action: str
    coordinate: Optional[List[int]] = None
    text: Optional[str] = None
    keys: Optional[str] = None

    def validate(self):
        """Validate the computer action parameters"""
        if self.action in ("mouse_move", "left_click_drag"):
            if self.coordinate is None:
                raise ScrapybaraError(f"coordinate is required for {self.action}")
            if self.text is not None:
                raise ScrapybaraError(f"text is not accepted for {self.action}")
            if not isinstance(self.coordinate, list) or len(self.coordinate) != 2:
                raise ScrapybaraError(f"{self.coordinate} must be a list of length 2")
            if not all(isinstance(i, int) and i >= 0 for i in self.coordinate):
                raise ScrapybaraError(
                    f"{self.coordinate} must be a list of non-negative ints"
                )

        if self.action in ("key", "type"):
            if self.text is None:
                raise ScrapybaraError(f"text is required for {self.action}")
            if self.coordinate is not None:
                raise ScrapybaraError(f"coordinate is not accepted for {self.action}")
            if not isinstance(self.text, str):
                raise ScrapybaraError(f"{self.text} must be a string")

        if self.action in (
            "left_click",
            "right_click",
            "double_click",
            "middle_click",
            "screenshot",
            "cursor_position",
        ):
            if self.text is not None:
                raise ScrapybaraError(f"text is not accepted for {self.action}")
            if self.coordinate is not None:
                raise ScrapybaraError(f"coordinate is not accepted for {self.action}")


@dataclass
class EditCommand:
    """
    File editing command data

    Attributes:
        command: Type of edit operation to perform
        path: Path to the target file
        content: Content for create command
        view_range: [start_line, end_line] for view command
        old_text: Text to replace for str_replace command
        new_text: New text for str_replace or insert commands
        line_number: Line number for insert command
    """

    command: Command
    path: str
    content: Optional[str] = None
    view_range: Optional[List[int]] = None
    old_text: Optional[str] = None
    new_text: Optional[str] = None
    line_number: Optional[int] = None

    def validate(self) -> None:
        """Validate the edit command parameters"""
        if self.command == "view":
            if self.view_range is not None:
                if not isinstance(self.view_range, list) or len(self.view_range) != 2:
                    raise ScrapybaraError("view_range must be a list of length 2")
                if not all(isinstance(i, int) and i >= 0 for i in self.view_range):
                    raise ScrapybaraError(
                        "view_range must be a list of non-negative integers"
                    )

        elif self.command == "create":
            if self.content is None:
                raise ScrapybaraError("content is required for create command")

        elif self.command == "str_replace":
            if self.old_text is None or self.new_text is None:
                raise ScrapybaraError(
                    "old_text and new_text are required for str_replace command"
                )

        elif self.command == "insert":
            if self.line_number is None or self.new_text is None:
                raise ScrapybaraError(
                    "line_number and new_text are required for insert command"
                )
            if not isinstance(self.line_number, int) or self.line_number < 0:
                raise ScrapybaraError("line_number must be a non-negative integer")


class ScrapybaraConfig:
    """
    Configuration for Scrapybara instance

    Args:
        base_url: Base URL for the Scrapybara service (default: http://localhost:8000)
        instance_type: AWS instance type (default: t4g.micro)
        region: AWS region (default: us-west-2)
    """

    def __init__(
        self,
        base_url: str = "https://starfish-app-e63cz.ondigitalocean.app",
        instance_type: str = "t4g.micro",
        region: str = "us-west-2",
    ):
        self.base_url = base_url.rstrip("/")
        self.instance_type = instance_type
        self.region = region


class Scrapybara:
    """
    Main class for interacting with the Scrapybara virtual desktop service

    Args:
        api_key: Authentication key for the Scrapybara service
        config: Optional configuration object (ScrapybaraConfig)
    """

    def __init__(self, api_key: str, config: Optional[ScrapybaraConfig] = None):
        self.api_key = api_key
        self.config = config or ScrapybaraConfig()
        self._instances: Dict[str, str] = {}

    def _headers(self):
        """Generate headers for API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _get_instance_url(self, instance_id: str) -> str:
        """
        Get instance URL, attempting to retrieve it via status if not in _instances

        Args:
            instance_id: ID of the instance to get URL for

        Returns:
            Instance URL

        Raises:
            ScrapybaraError: If instance doesn't exist or if status check fails
        """
        if instance_id not in self._instances:
            instance = self.status(instance_id)
            self._instances[instance_id] = f"http://{instance.public_ip}:8000"
        return self._instances[instance_id]

    def start(self) -> Instance:
        """
        Start a new virtual desktop instance

        Returns:
            Instance object containing instance details

        Raises:
            ScrapybaraError: If start fails
        """
        response = requests.post(
            f"{self.config.base_url}/deploy",
            headers=self._headers(),
            json={
                "instance_type": self.config.instance_type,
                "region": self.config.region,
            },
        )
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to start instance: {response.text}")

        data = response.json()
        instance = Instance(
            instance_id=data["instance_id"],
            public_ip=data["public_ip"],
            status=InstanceStatus(data["status"]),
        )
        self._instances[instance.instance_id] = f"http://{instance.public_ip}:8000"
        return instance

    def stop(self, instance_id: str) -> None:
        """
        Stop a virtual desktop instance

        Args:
            instance_id: ID of the instance to stop

        Raises:
            ScrapybaraError: If stop fails
        """
        response = requests.post(
            f"{self.config.base_url}/terminate/{instance_id}",
            headers=self._headers(),
        )
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to stop instance: {response.text}")

        if instance_id in self._instances:
            del self._instances[instance_id]

    def status(self, instance_id: str) -> Instance:
        """
        Get instance status

        Args:
            instance_id: ID of the instance to check

        Returns:
            Instance object containing current instance details

        Raises:
            ScrapybaraError: If status check fails
        """
        response = requests.get(
            f"{self.config.base_url}/status/{instance_id}",
            headers=self._headers(),
        )
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to get instance status: {response.text}")

        data = response.json()
        return Instance(
            instance_id=instance_id,
            public_ip=data["public_ip"],
            status=InstanceStatus(data["instance_state"]),
            launch_time=(
                datetime.fromisoformat(data["launch_time"])
                if data.get("launch_time")
                else None
            ),
        )

    def screenshot(self, instance_id: str) -> str:
        """
        Take a screenshot of the virtual desktop

        Args:
            instance_id: ID of the instance to screenshot

        Returns:
            Screenshot data as base64-encoded string

        Raises:
            ScrapybaraError: If instance doesn't exist or if screenshot fails
        """
        instance_url = self._get_instance_url(instance_id)
        response = requests.get(f"{instance_url}/screenshot")
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to take screenshot: {response.text}")
        return response.json()["base64_image"]

    def computer(
        self,
        instance_id: str,
        action: Action,
        coordinate: Optional[Tuple[int, int]] = None,
        text: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute a computer action (mouse/keyboard)

        Args:
            instance_id: ID of the instance to control
            action: Type of action to perform (see Action enum)
            coordinate: Optional (x, y) coordinates for mouse actions
            text: Optional text for keyboard actions

        Returns:
            Dict containing action result

        Raises:
            ScrapybaraError: If instance doesn't exist or if action fails
        """
        instance_url = self._get_instance_url(instance_id)
        computer_action = ComputerAction(
            action=action,
            coordinate=list(coordinate) if coordinate else None,
            text=text,
        )
        computer_action.validate()

        response = requests.post(
            f"{instance_url}/computer", json=computer_action.__dict__
        )
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to execute computer action: {response.text}")
        return response.json()

    def bash(
        self, instance_id: str, command: Optional[str] = None, restart: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a bash command or restart the bash session

        Args:
            instance_id: ID of the instance to run command on
            command: Shell command to execute
            restart: Whether to restart the bash session

        Returns:
            Dict containing command output

        Raises:
            ScrapybaraError: If instance doesn't exist or if command fails
        """
        instance_url = self._get_instance_url(instance_id)
        if restart:
            response = requests.post(f"{instance_url}/bash/restart")
            if response.status_code != 200:
                raise ScrapybaraError(f"Failed to restart bash: {response.text}")
            return response.json()

        if not command:
            raise ScrapybaraError("Command is required when not restarting")

        response = requests.post(f"{instance_url}/bash", json={"command": command})
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to execute bash command: {response.text}")
        return response.json()

    def edit(
        self,
        instance_id: str,
        command: Command,
        path: str,
        content: Optional[str] = None,
        view_range: Optional[List[int]] = None,
        old_text: Optional[str] = None,
        new_text: Optional[str] = None,
        line_number: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        File editing operations
        Commands:
        - view: View file content. Use view_range for specific lines
        - create: Create new file with content
        - str_replace: Replace old_text with new_text
        - insert: Insert new_text at line_number
        - undo_edit: Undo last edit operation

        Args:
            instance_id: ID of the instance to edit files on
            command: The edit command to execute
            path: Absolute path to the file
            content: File content for create command
            view_range: [start_line, end_line] for view command
            old_text: Text to replace for str_replace command
            new_text: New text for str_replace or insert commands
            line_number: Line number for insert command
        """
        instance_url = self._get_instance_url(instance_id)
        edit_command = EditCommand(
            command=command,
            path=path,
            content=content,
            view_range=view_range,
            old_text=old_text,
            new_text=new_text,
            line_number=line_number,
        )
        edit_command.validate()

        response = requests.post(f"{instance_url}/edit", json=edit_command.__dict__)
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to execute edit command: {response.text}")
        return response.json()
