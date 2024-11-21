from typing import Optional
import requests
from datetime import datetime
import time

from .models.types import Region, InstanceType
from .models.instance import Instance
from .models.config import ScrapybaraConfig
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

    def _headers(self):
        """Generate headers for API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

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
            f"{self.config.base_url}/instance/{instance_id}/status",
            headers=self._headers(),
        )
        if response.status_code != 200:
            raise ScrapybaraError(f"Failed to get instance status: {response.text}")

        data = response.json()

        return Instance(
            id=instance_id,
            launch_time=(
                datetime.fromisoformat(data["launch_time"].replace("Z", "+00:00"))
            ),
            region=data["region"],
            instance_type=data["instance_type"],
            _api_key=self.api_key,
            _base_url=self.config.base_url,
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
            id=data["instance_id"],
            launch_time=(
                datetime.fromisoformat(data["launch_time"].replace("Z", "+00:00"))
            ),
            region=data["region"],
            instance_type=data["instance_type"],
            _api_key=self.api_key,
            _base_url=self.config.base_url,
        )

        # Wait for both EC2 and Docker to be ready
        max_retries = 15
        retry_delay = 5

        for attempt in range(max_retries):
            status = instance.get_status()
            if status == "running":
                return instance
            time.sleep(retry_delay)

        return instance
