from typing import Optional, List
from pydantic import BaseModel, model_validator

from .types import Action
from .exceptions import ScrapybaraError


class ComputerAction(BaseModel):
    """Computer action request model"""

    action: Action
    coordinate: Optional[List[int]] = None
    text: Optional[str] = None

    @model_validator(mode="after")
    def validate_action_params(self) -> "ComputerAction":
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

        return self
