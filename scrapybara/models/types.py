from enum import Enum
from typing import Literal

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

Region = Literal[
    "us-east-1",
    "us-east-2",
    # ... rest of regions ...
]

InstanceType = Literal["small", "medium", "large"]


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
