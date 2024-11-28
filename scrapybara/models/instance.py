from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
from pydantic import BaseModel, PrivateAttr

from .types import Action, Command, InstanceStatus, InstanceType
from .computer_action import ComputerAction
from .edit_command import EditCommand
from .exceptions import ScrapybaraError
import requests


class Instance(BaseModel):
    """
    Virtual desktop instance

    Attributes:
        id: Unique identifier for the instance
        launch_time: When the instance was started
        instance_type: Type of instance
        _api_key: Authentication key for API requests (private)
        _base_url: Base URL for API requests (private)
    """

    id: str
    launch_time: datetime
    instance_type: InstanceType
    _api_key: str = PrivateAttr()
    _base_url: str = PrivateAttr()
    _browser: Optional["Instance.Browser"] = PrivateAttr(default=None)

    def __init__(self, **data):
        super().__init__(**data)
        self._api_key = data.get("_api_key")
        self._base_url = data.get("_base_url")

    def _headers(self):
        """Generate headers for API requests"""
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    def screenshot(self) -> str:
        """Take a screenshot of the virtual desktop"""
        response = requests.get(
            f"{self._base_url}/instance/{self.id}/screenshot",
            headers=self._headers(),
        )
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to take screenshot: {response.text}")
        return response.json()["base64_image"]

    def computer(
        self,
        action: Action,
        coordinate: Optional[Tuple[int, int]] = None,
        text: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute a computer action (mouse/keyboard)"""
        computer_action = ComputerAction(
            action=action,
            coordinate=list(coordinate) if coordinate else None,
            text=text,
        )

        response = requests.post(
            f"{self._base_url}/instance/{self.id}/computer",
            json=computer_action.__dict__,
            headers=self._headers(),
        )
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to execute computer action: {response.text}")
        return response.json()

    def bash(
        self, command: Optional[str] = None, restart: bool = False
    ) -> Dict[str, Any]:
        """Execute a bash command or restart the bash session"""
        if restart:
            response = requests.post(
                f"{self._base_url}/instance/{self.id}/bash/restart",
                headers=self._headers(),
            )
            if response.status_code != 200:
                raise ScrapybaraError(f"Failed to restart bash: {response.text}")
            return response.json()

        if not command:
            raise ScrapybaraError("Command is required when not restarting")

        response = requests.post(
            f"{self._base_url}/instance/{self.id}/bash",
            json={"command": command},
            headers=self._headers(),
        )
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to execute bash command: {response.text}")
        return response.json()

    def edit(
        self,
        command: Command,
        path: str,
        file_text: Optional[str] = None,
        view_range: Optional[List[int]] = None,
        old_str: Optional[str] = None,
        new_str: Optional[str] = None,
        insert_line: Optional[int] = None,
    ) -> Dict[str, Any]:
        """File editing operations"""
        edit_command = EditCommand(
            command=command,
            path=path,
            file_text=file_text,
            view_range=view_range,
            old_str=old_str,
            new_str=new_str,
            insert_line=insert_line,
        )

        response = requests.post(
            f"{self._base_url}/instance/{self.id}/edit",
            json=edit_command.__dict__,
            headers=self._headers(),
        )
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to execute edit command: {response.text}")
        return response.json()

    def stop(self) -> None:
        """Stop this virtual desktop instance"""
        response = requests.post(
            f"{self._base_url}/instance/{self.id}/terminate",
            headers=self._headers(),
        )
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to stop instance: {response.text}")

    def get_stream_url(self) -> str:
        """Get NoVNC stream URL for the instance"""
        response = requests.get(
            f"{self._base_url}/instance/{self.id}/stream_url",
            headers=self._headers(),
        )
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to get stream URL: {response.text}")
        return response.json()["stream_url"]

    def get_status(self) -> InstanceStatus:
        """Get instance status"""
        response = requests.get(
            f"{self._base_url}/instance/{self.id}/status",
            headers=self._headers(),
        )
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to get instance status: {response.text}")
        return response.json()["instance_state"]

    class Browser:
        """Browser API for the virtual desktop instance"""

        def __init__(self, instance: "Instance"):
            self.instance = instance

        def start(self) -> str:
            """Start a browser session"""
            response = requests.post(
                f"{self.instance._base_url}/instance/{self.instance.id}/browser/start",
                headers=self.instance._headers(),
            )
            if response.status_code != 200:
                raise ScrapybaraError(f"Failed to start browser: {response.text}")
            return response.json()["cdp_endpoint"]

        def get_cdp_url(self) -> str:
            """Get the CDP URL for the browser session"""
            response = requests.get(
                f"{self.instance._base_url}/instance/{self.instance.id}/browser/cdp_url",
                headers=self.instance._headers(),
            )
            if response.status_code != 200:
                raise ScrapybaraError(f"Failed to get CDP URL: {response.text}")
            return response.json()["cdp_endpoint"]

        def stop(self) -> None:
            """Stop the browser session"""
            response = requests.post(
                f"{self.instance._base_url}/instance/{self.instance.id}/browser/stop",
                headers=self.instance._headers(),
            )
            if response.status_code != 200:
                raise ScrapybaraError(f"Failed to stop browser: {response.text}")

    @property
    def browser(self) -> Browser:
        if self._browser is None:
            self._browser = self.Browser(self)
        return self._browser
