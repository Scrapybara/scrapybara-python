from typing import Optional, List
from pydantic import BaseModel, model_validator

from .types import Command
from .exceptions import ScrapybaraError


class EditCommand(BaseModel):
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

    @model_validator(mode="after")
    def validate_command_params(self) -> "EditCommand":
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

        return self
