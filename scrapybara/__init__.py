from typing import Optional, Dict, Any, List, Tuple
import requests
from datetime import datetime
import time

from .models.types import Action, Command, Region, InstanceType, InstanceStatus
from .models.instance import Instance
from .models.config import ScrapybaraConfig
from .models.computer_action import ComputerAction
from .models.edit_command import EditCommand
from .models.exceptions import ScrapybaraError


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
            instance = self.get(instance_id)
            self._instances[instance_id] = f"http://{instance.public_ip}:8000"
        return self._instances[instance_id]

    def get(self, instance_id: str) -> Instance:
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
        instance_state = InstanceStatus(data["instance_state"])

        if instance_state == InstanceStatus.RUNNING:
            instance_url = f"http://{data['public_ip']}:8000"
            try:
                status_response = requests.get(f"{instance_url}/status", timeout=5)
                if (
                    status_response.status_code != 200
                    or status_response.json().get("status") != "ok"
                ):
                    instance_state = InstanceStatus.DEPLOYING
            except (requests.exceptions.RequestException, ValueError):
                instance_state = InstanceStatus.DEPLOYING

        return Instance(
            instance_id=instance_id,
            public_ip=data["public_ip"],
            status=instance_state,
            launch_time=(
                datetime.fromisoformat(data["launch_time"].replace('Z', '+00:00'))
                if data.get("launch_time")
                else None
            ),
        )

    def start(
        self, instance_type: InstanceType = "small", region: Region = "us-west-2"
    ) -> Instance:
        """
        Start a new virtual desktop instance and wait for it to be fully ready

        Args:
            instance_type: Size of the instance (small, medium, large)
            region: Region to deploy the instance in

        Returns:
            Instance object containing instance details

        Raises:
            ScrapybaraError: If start fails or instance doesn't become ready within timeout
        """
        # Initial instance deployment
        response = requests.post(
            f"{self.config.base_url}/deploy",
            headers=self._headers(),
            json={
                "instance_type": instance_type,
                "region": region,
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

        # Wait for both EC2 and Docker to be ready
        max_retries = 15
        retry_delay = 5

        for attempt in range(max_retries):
            instance = self.get(instance.instance_id)
            if instance.status == InstanceStatus.RUNNING:
                return instance
            
            print(f"Instance not ready, retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(retry_delay)
        
        return instance
        # raise ScrapybaraError("Instance failed to become ready within timeout period")

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
        file_text: Optional[str] = None,
        view_range: Optional[List[int]] = None,
        old_str: Optional[str] = None,
        new_str: Optional[str] = None,
        insert_line: Optional[int] = None,
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
            file_text: File content for create command
            view_range: [start_line, end_line] for view command
            old_str: Text to replace for str_replace command
            new_str: New text for str_replace or insert commands
            insert_line: Line number for insert command
        """
        instance_url = self._get_instance_url(instance_id)
        edit_command = EditCommand(
            command=command,
            path=path,
            file_text=file_text,
            view_range=view_range,
            old_str=old_str,
            new_str=new_str,
            insert_line=insert_line,
        )

        response = requests.post(f"{instance_url}/edit", json=edit_command.__dict__)
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to execute edit command: {response.text}")
        return response.json()
