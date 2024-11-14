from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from .types import InstanceStatus


class Instance(BaseModel):
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
