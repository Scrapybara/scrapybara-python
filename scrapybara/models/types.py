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
    "us-west-1",
    "us-west-2",
]

InstanceType = Literal["small", "medium", "large"]

InstanceStatus = Literal[
    "deploying",
    "running",
    "terminated",
    "error",
]
